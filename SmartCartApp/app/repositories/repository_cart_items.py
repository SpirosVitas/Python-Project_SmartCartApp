import sqlite3
from app.model.cart_item import CartItem    # Εισαγωγή του μοντέλου CartItem


class CartItemRepository:
    # Constructor δημιουργεί σύνδεση με τη βάση δεδομένων
    def __init__(self, db_path = "smartcart.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row


    # Προσθέτει προϊόν στο καλάθι ή αυξάνει την ποσότητα αν υπάρχει ήδη
    def add_to_cart(self, cart_item: CartItem):
        cursor = self.conn.cursor()

        # Ελέγχει αν υπάρχει ήδη το προϊόν στο καλάθι
        cursor.execute("SELECT quantity FROM cart_items WHERE product_id = ?", (cart_item.product_id,))
        row = cursor.fetchone()

        if row:
            # Αν υπάρχει, ενημερώνει την ποσότητα
            new_quantity = row["quantity"] + cart_item.quantity
            cursor.execute("UPDATE cart_items SET quantity = ? WHERE product_id = ?", (new_quantity, cart_item.product_id))
        else:
             # Αν δεν υπάρχει, το εισάγει ως νέο
            cursor.execute(
                "INSERT INTO cart_items (product_id, product_name, quantity, price) VALUES (?, ?, ?, ?)",
                (cart_item.product_id, cart_item.product_name, cart_item.quantity, cart_item.price)
            )
                       
        self.conn.commit()  # Αποθηκεύει τις αλλαγές


    # Επιστρέφει όλα τα προϊόντα του καλαθιού ως λίστα αντικειμένων CartItem
    def get_cart_items(self) -> list[CartItem]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM cart_items")
        rows = cursor.fetchall()
        return[CartItem.from_dict(dict(row)) for row in rows]   # Κάθε γραμμή γίνεται αντικείμενο CartItem 



    # Αφαιρεί ένα προϊόν από το καλάθι με το product_id
    def remove_from_cart(self, product_id: int):
         cursor = self.conn.cursor()
         cursor.execute("DELETE FROM cart_items WHERE product_id = ?", (product_id,))
         self.conn.commit()
         return cursor.rowcount > 0


    # Αδειάζει το καλάθι
    def clear_cart(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM cart_items")
        self.conn.commit()


    # Ενημερώνει την ποσότητα ενός προϊόντος στο καλάθι
    def update_quantity(self, product_id: int, new_quantity: int):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            UPDATE cart_items
            SET quantity = ?
            WHERE product_id = ?
            ''',
            (new_quantity, product_id)
        )
        self.conn.commit()
        return cursor.rowcount > 0 
