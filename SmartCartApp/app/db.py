import os,  sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # Ορίζει τον φάκελο στον οποίο βρίσκεται το παρόν αρχείο
DB_PATH = os.path.join(BASE_DIR, "..", "smartcart.db")  # Δημιουργεί το path για τη βάση δεδομένων "smartcart.db"

# Σύνδεση με την βάση δεδομένων
def connect_db():
    conn = sqlite3.connect(DB_PATH) # Δημιουργεί σύνδεση με τη βάση
    conn.row_factory = sqlite3.Row  # Επιστρέφει αποτελέσματα σαν dictionaries αντί για tuples
    conn.execute("PRAGMA foreign_keys = ON")    # Ενεργοποιεί τα ξένα κλειδιά
    return conn # Επιστρέφει το connection object

print("DB Created")
