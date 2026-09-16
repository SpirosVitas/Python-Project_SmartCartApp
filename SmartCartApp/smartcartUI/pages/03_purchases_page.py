import streamlit as st
import requests

API_PURCHASE_URL = "http://localhost:7000/purchases"    # route για προηγούμενες αγορές

st.set_page_config(page_title="Προηγούμενες Αγορές", layout="wide")
st.title("Προηγούμενες Αγορές")

# Ανάκτηση προηγούμενων αγορών
def fetch_purchases():
    try:
        response = requests.get(API_PURCHASE_URL, timeout=20)    # Κάνει το get request
        response.raise_for_status()
        return response.json()  # Επιστρέφει τις αγορές
    except Exception as e:
        st.error(f"Σφάλμα κατά την ανάκτηση των αγορών: {e}")
        return []
    
purchases = fetch_purchases()

# Αν υπάρχουν αγορές
if purchases:   
    for purchase in purchases:  # Για κάθε αγορά
        # Expnader με τις πληροφορίες αγοράς
        with st.expander(f"Κωδικός Αγοράς {purchase['id']} | {purchase['created_at']} | {purchase['total_price']}€"):
            # Κουμπι για εμφάνιση προίοντων συγκεκριμένης αγορας
            if st.button(f"Δες τα προιόντα για {purchase['id']}", key=f"show_{purchase['id']}"):
                st.markdown("**Προιόντα:**")
                try:
                    detail_response = requests.get(f"{API_PURCHASE_URL}/{purchase['id']}", timeout=20)  # Κάνει το get request παίρνει και βάζει στο path το purchase_id
                    detail_response.raise_for_status()
                    purchase_items = detail_response.json() # Επιστρέφει τα προιόντα

                    # Για κάθε προιόν εμφανίζει τις πληροφορίες του 
                    for purchase_item in purchase_items:    
                        st.markdown (f"**{purchase_item['product_name']}** (Κωδ: {purchase_item['product_id']}) - "
                                 f"{purchase_item['quantity']} τμχ x {purchase_item['price']}€")
                except Exception as e:
                        st.error(f"Σφάλμα κατά την ανάκτηση προιόντων: {e}")
    else:   # Αν δεν υπάρχουν προηγούμενες αγορές εμφανίζει το ανάλογο μήνυμα
        st.info("Δεν υπάρχουν προηγούμενες αγορες")
