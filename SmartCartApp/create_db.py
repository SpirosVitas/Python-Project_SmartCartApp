import sqlite3

def create_tables():    # Φτιάχνει τους πίνακες της βάσης δεδομένων
    conn = sqlite3.connect("smartcart.db")  # Συνδέεται με την βάση
    cursor = conn.cursor()  # Δημιουργεί cursor για εκτέλεση SQL εντολών

    # Δημιουργεί τον πίνακα των προιόντων
    cursor.execute('''  
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT NOT NULL,
            price FLOAT NOT NULL,
            image_url TEXT
            
        );
    ''')


    # Δημιουργεί τον πίνακα των προιόντων του καλαθιού
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cart_items (
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price FLOAT NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id)
        );
    ''')

    # Δημιουργεί τον πίνακα των αγορών
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY,       
            created_at TEXT NOT NULL,  
            total_price FLOAT NOT NULL
        );
    ''')

    # Δημιουργεί τον πίνακα των προιόντων των αγορών
    cursor.execute('''
         CREATE TABLE IF NOT EXISTS purchase_items (
            id INTEGER PRIMARY KEY,
            purchase_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            price FLOAT NOT NULL,
            FOREIGN KEY (purchase_id) REFERENCES purchases(id)
        );
    ''')
      

    conn.commit()   # Αποθηκεύει τις αλλαγές
    conn.close()       # Κλείνει τη σύνδεση
    print("DB tables created")

    # Το αρχείο εκτελείτε μόνο από εδω
if __name__ == "__main__":
        create_tables()
