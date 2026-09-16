import pandas as pd # Χρήση της pandas για ανάγνωση αρχείου CSV
import sqlite3      # Χρήση sqlite3 για σύνδεση με SQLite DB

CSV_FILE = "UniShop.csv"    # Ορισμός διαδρομής αρχείου CSV με προϊόντα
DB_FILE = "smartcart.db"    # Ορισμός διαδρομής βάσης δεδομένων

def import_products():  # Εισάγει τα προιόντα
    df = pd.read_csv(CSV_FILE, delimiter=';')   # Διαβάζει το CSV με διαχωριστικό ;

    # Ελέγχει ότι το CSV περιλαμβάνει όλες τις απαιτούμενες στήλες
    required_columns = {"id", "name", "description", "category", "price", "image_url"}
    if not required_columns.issubset(set(df.columns)):
        print(f"Το CSV πρεπει να εχει τις στηλες: {required_columns}")
        return

    conn = sqlite3.connect(DB_FILE) # Συνδέεται στη βάση SQLite
    cursor = conn.cursor()          # Δημιουργεί cursor για εκτέλεση SQL εντολών

    for _, row in df.iterrows():    # Για κάθε γραμμή 
       # Εκχωρεί στο πίνακα των προιόντων
       cursor.execute('''
            INSERT INTO products (id, name, description, category, price, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            row['id'],
            row['name'],
            row['description'],
            row['category'],
            float(row['price']),
            row['image_url']
        ))   
       
    conn.commit()   # Αποθηκεύει τις αλλαγές
    conn.close()    # Κλείνει τη σύνδεση
    print("Products Inserted")   

# Το αρχείο εκτελείτε μόνο από εδω
if __name__ == "__main__":
    import_products ()   
