import streamlit as st
import pandas as pd
import numpy as np
import requests


API_CART_URL = "http://localhost:7000/cart"         # route προβολή και ενημέρωσης ποσότητας καλαθιού
API_REMOVE_URL = "http://localhost:7000/cart/item"  # route διαγραφή προιόντων καλαθιού
API_PURCHASE_URL = "http://localhost:7000/purchase" # route για ολοκλήρωση αγοράς
API_AI_URL = "http://localhost:7000/ai/evaluate"    # route για αξιολόγηση καλαθιού

st.set_page_config(page_title="Καλάθι", layout="wide")
st.title("Το Καλάθι μου")


def show_cart():    # Ανάκτηση πριόντων καλαθιού
    try:
        response = requests.get(API_CART_URL, timeout=20)   # Κάνει το get request, αν περάσουν 20 δευτερόλεπτα σταματάει
        response.raise_for_status()  # Αν το status code διαφορετικό απο το 200 πετάει exception
        return response.json()  # Επιστρέφει την λίστα των προιόντων
    except Exception as e:
        st.error(f"Σφάλμα εμφάνισης καλαθιού: {e} ")
        return []
    

def update_quantity(product_id, quantity):  # Ενημέρωση ποσότητας
    payload = { # Παίρνει product_id και quantity
        "product_id": product_id,
        "quantity": quantity
    }
    try:
        response = requests.put(API_CART_URL, json=payload, timeout=20) # Κάνει το put request
        if response.status_code == 200: # Αν επιτυχία
            st.success("Η ποσότητα ενημερώθηκε")
        else:
            st.error(f"Σφάλμα: {response.json().get('error')}")    # Σφάλμα API πχ. δεν πήρε το σωστό id
    except Exception as e:
        st.error(f"Σφάλμα κατά την ενημέρωση: {e}")     # Σφάλμα κατά το αίτημα 


def delete_item(product_id):    # Διαγραφή προιόντος
    try:
        response = requests.delete(f"{API_REMOVE_URL}?product_id={product_id}", timeout=20) # Κάνει το delete request, παίρνοντας το id και το βάζει παράμετρο στο url
        if response.status_code == 200:
            st.success("Το προϊόν αφαιρέθηκε από το καλάθι")
        else:
            st.error(f"Σφάλμα: {response.json().get('error')}")
    except Exception as e:
        st.error(f"Σφάλμα διαγραφής: {e}")


def clear_cart():   # Διαγραφή καλαθιού
    try:
        response = requests.delete(API_CART_URL, timeout=20)    # Κάνει το delete request
        if response.status_code == 200:
            st.success(f"Το καλάθι άδειασε")
        else:
            st.error("Αποτυχία εκκαθάρισης")
    except Exception as e:
        st.error(f"Σφάλμα: {e}")
    
cart_items = show_cart()    # Ανάκτηση πορόντων καλαθιού
total_price = 0.0   # Αρχικοποίηση συνολικής τιμής

# Αν το καλάθι είναι άδειο εμφάνισε μήνυμα
if not isinstance(cart_items, list) or len(cart_items) == 0:
    st.info("Το καλάθι είναι άδειο")
else:   # αλλιώς για κάθε προιόν στο καλάθι
    for cart_item in cart_items:
        with st.container():    # το κάθε προιόν σε container
            cols = st.columns([3, 2, 2, 2, 1, 1])   # Στήλες για εμφάνιση 

            # Όνομα και id στην πρώτη στήλη
            cols[0].markdown(f"### {cart_item['product_name']}")
            cols[0].markdown(f"**Κωδικός**: {cart_item['product_id']}")
            # Τιμή στη δεύτερη στήλη
            cols[1].markdown(f"**Τιμή**: {cart_item['price']} €")

            # Ποσότητα με number input (+/-) στην τρίτη στήλη
            quantity = cols[2].number_input(
                "Ποσότητα", min_value=1, value=cart_item["quantity"], key=f"qty_{cart_item['product_id']}"
            )

            # Κουμπί ενημέρωσης ποόσοτητάς που κάλει το Api που αλλάζει την ποσότητα στην τέταρτη στήλη
            if cols[3].button("Ενημέρωση", key=f"update_{cart_item['product_id']}"):
                update_quantity(cart_item["product_id"], quantity)
                st.rerun()  # Αν πατηθεί το κουμπί ξανατρέχει η σελίδα

            # Κουμπί διαγραφής που κάλει το api που διαγράφςι το προιόν στην πεμπτη στήλη
            if cols[4].button("Διαγραφή", key=f"delete_{cart_item['product_id']}"):
                delete_item(cart_item["product_id"])
                st.rerun()

            total_price += cart_item["price"] * cart_item["quantity"] # Υπολογισμος συνολικής τιμής

    st.markdown("---")
    st.divider()
    st.markdown(f"###Συνολική Τιμή: **{total_price:.2f} €**") # Εμφάνιση συνολικής τιμής

    # Κουμπί για ολοκλήρωση αγοράς
    if st.button("Ολοκλήρωση αγοράς"):
        try:
            response = requests.post(API_PURCHASE_URL, timeout=20) # Κάνει το post request
            if response.status_code == 201: # Αν επιτυχία
                st.success("Η αγορά ολοκληρώθηκε επιτυχώς")
                st.rerun()  # Επαναφόρτωση σελίδας
            else:
                st.error(f"Σφάλμα: {response.json().get('error')}")
        except Exception as e:
            st.error(f"Σφαλμά κατά την αγορά")
   
    # Κουμπί για άδειασμα καλαθιού
    if st.button("Άδειασμα Καλαθιού"):
        clear_cart()
        st.rerun()


    # Κουμπι για αξιολόγηση
    if st.button("Αξιολογησή καλαθιού"):
        with st.spinner("Γίνεται αξιολόγηση..."):
            try:
                response = requests.get(API_AI_URL, timeout=20) # Κάνει το get request
                data = response.json()
                if response.status_code == 200: # Αν επιτυχία
                    st.success("Η αξιολόγηση ολοκληρώθηκε")
                    for cart_item in data["cart"]:  # Λίστα πριόντων που αξιολογήθηκαν 
                        st.markdown(f"{cart_item['quantity']} x **{cart_item['name']}** (*{cart_item['category']}*)")
                else:
                    st.error(f"{data.get('error', 'Σφαλμα')}")
            except Exception as e:
                st.error(f"Σφάλμα: {e}")
            st.info(data['evaluation'])     # Εμφάνιση αξιολόγησης




