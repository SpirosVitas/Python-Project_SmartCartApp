import sqlite3
from app.model.purchase import Purchase             # Εισαγωγή του μοντέλου Purchase
from app.model.purchase_item import PurchaseItem    # Εισαγωγή του μοντέλου PurchaseItem

class PurchaseRepository:
    # Constructor δημιουργεί σύνδεση με τη βάση δεδομένων
    def __init__(self, db_path="smartcart.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
    

    # Δημιουργεί νέα αγορά και εισάγει τα προϊόντα που αγοράστηκαν
    def create_purchase(self, purchase: Purchase, items: list[PurchaseItem]):
        cursor = self.conn.cursor()

        # Εισαγωγή της αγοράς στον πίνακα purchases
        cursor.execute ('''
            INSERT INTO purchases (id, created_at, total_price)
            VALUES (?, ?, ?)
        ''', (purchase.id, purchase.created_at, purchase.total_price))

        # Εισαγωγή των προιόντων της αγοράς στον πίνακα purchase_items
        for item in items:
            cursor.execute ('''
                INSERT INTO purchase_items (purchase_id, product_id, product_name, quantity, price)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                item.purchase_id, item.product_id,
                item.product_name, item.quantity, item.price
            ))

        self.conn.commit()    # Αποθηκεύει τις αλλαγές


    # Επιστρέφει όλες τις αγορές ταξινομημένες από τις πιο πρόσφατες
    def get_all_purchases(self) -> list[Purchase]: 
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM purchases ORDER BY created_at DESC")
        # Μετατροπή των αποτελεσμάτων σε αντικείμενα Purchase και ανάκτηση όλων
        return [Purchase.from_dict(dict(row)) for row in cursor.fetchall()]


    # Επιστρέφει όλα τα προϊόντα μιας συγκεκριμένης αγοράς
    def get_purchase_items(self, purchase_id) -> list[PurchaseItem]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM purchase_items WHERE purchase_id = ?", (purchase_id,))
        # Μετατροπή των αποτελεσμάτων σε αντικείμενα PurchaseItem και ανάκτηση όλων
        return [PurchaseItem.from_dict(dict(row)) for row in cursor.fetchall()]    
    

    # Επιστρέφει όλα τα προϊόντα από όλες τις αγορές
    def get_all_purchase_items(self) -> list[PurchaseItem]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM purchase_items ORDER BY purchase_id DESC")
        return [PurchaseItem.from_dict(dict(row)) for row in cursor.fetchall()]
