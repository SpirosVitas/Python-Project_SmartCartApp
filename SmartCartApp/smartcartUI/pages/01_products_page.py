import streamlit as st
import requests
import pandas as pd



API_PRODUCTS_URL = "http://localhost:7000/products" # route για ανάκτηση προιόντων
API_CART_URL = "http://localhost:7000/cart"         # route για προσθήκη στο καλάθι

st.set_page_config(page_title="Προϊόντα", layout="wide")
st.title("Προϊόντα")


@st.cache_data(ttl=600) # Κασάρει τα αποτελέσματα για 10 λεπτά για μην γίνονται συνέχεια αιτήματα
def fetch_products():   # Ανάκτηση προιόντων
    try:
        response = requests.get(API_PRODUCTS_URL, timeout=20) # Κάνει το get request, αν περάσουν 20 δευτερόλεπτα σταματάει
        response.raise_for_status() # Αν το status code διαφορετικό απο το 200 πετάει exception
        return response.json()
    except Exception as e:
        st.error(f"Σφάλμα ανάκτησης δεδομένων από το API: {e}")
        return []
    
products = fetch_products()

# Αν υπάρχουν προιόντα
if products:
    # Φίλτρα στο sidebar 
    with st.sidebar:
        st.header("Φίλτρα")
        search_bar = st.text_input("Αναζήτηση προιόντος", "")   # Search field για αναζήτηση με το όνομα
        categories = sorted(set(p["category"] for p in products))
        selected_categories = st.multiselect("Κατηγορίες", categories, default=categories)  # Επιλογή κατηγορίας με multiselect
        price_min, price_max = st.slider("Εύρος Τιμής", 0, 2000, (0, 2000)) # Αναζήτηση για την τιμή με slider

    # Εμφάνιση προϊόντων αν βρίσκεται μέσα σε :
    for product in products:
        if (
            product["category"] in selected_categories and
            price_min <= product["price"] <= price_max and
            search_bar.lower() in product['name'].lower()
        ):
            with st.container():    # Εμφάνιση προιόντων πάνω σε container
                cols = st.columns([3, 2, 1])
                
                cols[0].markdown(f"### {product['name']}")
                cols[0].markdown(f"**Κωδικός**: {product['id']}")
                cols[0].markdown(f"*Κατηγορία*: {product['category']}")
                cols[0].markdown(f"*Περιγραφή*: {product.get('description', 'Χωρίς περιγραφή')}")
                cols[0].markdown(f"**Τιμή**: {product['price']} €")

                if product.get("image_url"):
                    cols[1].image(product["image_url"], width=150)

                if cols[2].button("Προσθήκη", key=f"add_{product['id']}"): # Κουμπι για προσθήκη στο καλάθι
                    payload = {
                        "product_id": product["id"],    # Παίρνει το product_id και αυξάνει την ποσότητα κατά 1
                        "quantity": 1
                    }

                    try:
                        response = requests.post(API_CART_URL, json=payload, timeout=20)   # Κάνει το post request μόλις πατηθεί το κουμπί
                        if response.status_code == 201: # Αν επιτυχία 
                            st.success(f"Προστέθηκε: {product['name']}")
                        else:
                            st.error(f"Αποτυχία: {response.json().get('error', 'Σφάλμα')}")
                    except Exception as e:
                        st.error(f"Σφάλμα αποστολής στο καλάθι: {e}")    
