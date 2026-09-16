import sqlite3  # Εισαγωγή βιβλιοθήκης για σύνδεση με sqlite βάση δεδομένων
import requests # Εισαγωγή βιβλιοθήκης για κλήσεις http
import json     # Εισαγωγή βιβλιοθήκης για διαχείριση Json 

GROQ_API_KEY = "*******************"

class AIRepository:
    # Constructor δημιουργεί σύνδεση με τη βάση δεδομένων
    def __init__(self, db_path="smartcart.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row

    # Μέθοδος για αποστολή prompt στο GROQ API
    def groq(self, prompt):
        url = "https://api.groq.com/openai/v1/chat/completions"
        data = {
            "messages": [{"role": "system", "content": "Απάντησε σύντομα και στα ελληνικά"},
                        {"role": "user", "content": prompt}],
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "temperature": 1,
            "max_completion_tokens": 1024,
            "top_p": 1,
            "stream": False,
        }
        # Δημιουργία JSON και headers για το POST request
        json_data = json.dumps(data)
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {GROQ_API_KEY}",
        }

        # Παιρνει τη απάντηση από το request
        response = requests.post(url, data=json_data, headers=headers)
        if response.status_code == 200: # Αν η κλήση επιτυχής 
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise Exception(f"GROQ API Error: {response.status_code} - {response.text}")

    # Ανάκτηση καλαθιού
    def get_cart_items(self):
       
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT p.category, p.name, ci.quantity
            FROM cart_items ci
            JOIN products p ON ci.product_id = p.id
        """)
        rows = cursor.fetchall()
        

        # Επιστροφή ως λίστα λεξικών
        return [{"category": row["category"], "name": row["name"], "quantity": row["quantity"]} for row in rows]
    

    # Γίνεται η αξιολόγηση
    def rate_cart(self):
        cart_items = self.get_cart_items()

        if not cart_items:
            return None, "The Cart is Empty"

        # Δημιουργεί prompt 
        product_list = ", ".join(f"{item['category']} {item['quantity']} x {item['name']}" for item in cart_items)
        prompt = f"Αξιολόγησε ως προς την ποιότητα το καλάθι μου που περιέχει: {product_list}"
        answer = self.groq(prompt)  # Στέλνει το prompt και επιστρέφει την απάντηση

        return cart_items, answer   # Επιστρέφει το καλάθι και την αξιολόγηση

