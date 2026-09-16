import streamlit as st
import requests

API_PRODUCTS_URL = "http://localhost:7000/products" # route για ανάκτηση προιόντων
API_SCRAPING_URL = "http://localhost:7000/scraping" # route για scraping

st.set_page_config(page_title="Web Scraping", layout="wide")
st.title("Scraping Προιόντων")

@st.cache_data(ttl=600) # Κασάρει τα αποτελέσματα για 10 λεπτά για μην γίνονται συνέχεια αιτήματα
def fetch_products():   # Ανάκτηση προιόντων
    try:
        response = requests.get(API_PRODUCTS_URL, timeout=20)   # Κάνει το get request, αν περάσουν 20 δευτερόλεπτα σταματάει
        response.raise_for_status()
        return response.json()  # Επιστρέφει λίστα προιόντων
    except Exception as e:
        st.error(f"Σφάλμα ανάκτησης δεδομένων από το API: {e}")
        return []
    
products = fetch_products()

# Αν δεν υπάρχουν προιόντα
if not products:
    st.info("Δεν βρέθηκαν προιόντα")
else:   # Αν υπάρχουν προιόντα
    for product in products:
        with st.container():    # Εμφάνιση κάθε προιόν σε container
                cols = st.columns([3, 2, 1])    # Στήλες για εμφάνιση
                
                # Πρώτη στήλη όνομα, id, κατηγορία, περιγρφήν τιμή
                cols[0].markdown(f"### {product['name']}")
                cols[0].markdown(f"**Κωδικός**: {product['id']}")
                cols[0].markdown(f"*Κατηγορία*: {product['category']}")
                cols[0].markdown(f"*Περιγραφή*: {product.get('description', 'Χωρίς περιγραφή')}")
                cols[0].markdown(f"**Τιμή**: {product['price']} €")

                # Δευτερή στήλη εικόνα αν υπάρχει
                if product.get("image_url"):
                    cols[1].image(product["image_url"], width=150)

                # Τρίτη στήλη κουμπί scraping 
                if cols[2].button("Scraping", key=f"scrape_{product['id']}"):
                    try:
                        params = {"product": product["name"], "category": product["category"]}  # Παίρνει τις παραμέτρους
                        response = requests.get(API_SCRAPING_URL, params=params, timeout=20)    # Κάνει το get request
                        data = response.json()  # Αποτελέσματα scraping

                        # Αν error η message εμφάνιση warning
                        if "error" in data or "message" in data:
                            st.warning(data.get("error") or data.get("message"))
                        else:   # Αλλιώς εμφανίzει τα αποτελέσματα του scraping
                            st.success(" Αποτελέσματα scraping:")
                            st.markdown(f"**Όνομα**: {data['name']}")
                            st.markdown(f"**Περιγραφή**: {data['description']}")
                            st.markdown(f"**Τιμή**: {data['price']}")
                            if data.get("image_url"):
                                st.image(data["image_url"], width=150)
                    except Exception as e:
                        st.error(f" Σφάλμα scraping: {e}")
