import streamlit as st
import requests

st.set_page_config(page_title="Αναλύσεις", layout="wide")

st.title("Αναλύσεις Πωλήσεων")

# Δημοιυργία τριων tabs
tab1, tab2, tab3 = st.tabs([
    "Top 5 Προϊόντα",
    "Κορυφαία ανά Κατηγορία",
    "Πρόβλεψη Πωλήσεων"
])

# Στο πρώτο tab
with tab1:
    st.subheader("Top 5 σε Πωλήσεις")   # Υπότιτλος
    try:
        response = requests.get("http://localhost:7000/analysis/top_products/chart", timeout=20)    # Κάνει το get request
        response.raise_for_status() # Έλεγχος για σφάλμα
        st.image(response.content, use_container_width=True)    # Εμφάνιση εικόνας σε όλη την οθόνη
    except Exception as e:
        st.error(f"Σφάλμα φόρτωσης: {e}")   # Μήνυμα σφάλματος αν αποτύχει

# Στο δεύτερο tab
with tab2:
    st.subheader("Καλύτερα Προϊόντα ανά Κατηγορία") # Υπότιτλος
    try:
        response = requests.get("http://localhost:7000/analysis/top_products_per_category/chart", timeout=20)   # Κάνει το get request
        response.raise_for_status() # Έλεγχος για σφάλμα
        st.image(response.content, use_container_width=True)    # Εμφάνιση εικόνας σε όλη την οθόνη
    except Exception as e:
        st.error(f"Σφάλμα φόρτωσης: {e}")   # Μήνυμα σφάλματος αν αποτύχει

# Στο τρίτο tab
with tab3:
    st.subheader("Πρόβλεψη Πωλήσεων ανά Ημέρα") # Υπότιτλος
    try:
        response = requests.get("http://localhost:7000/analysis/predict_sales/chart", timeout=20)   # Κάνει το get request
        response.raise_for_status() # Έλεγχος για σφάλμα
        st.image(response.content, use_container_width=True)    # Εμφάνιση εικόνας σε όλη την οθόνη
    except Exception as e:
        st.error(f"Σφάλμα φόρτωσης: {e}")    # Μήνυμα σφάλματος αν αποτύχει
