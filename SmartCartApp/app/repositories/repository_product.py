import sqlite3
from app.model.product import Product   # Εισαγωγή του μοντέλου Product

class ProductRepository:
    # Constructor δημιουργεί σύνδεση με τη βάση δεδομένων
    def __init__(self, db_path = "smartcart.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)    # Δημιουργία σύνδεσης με τη βάση
        self.conn.row_factory = sqlite3.Row # Επιτρέπει την πρόσβαση στα πεδία της βάσης ως dictionary όχι μόνο ως tuple
    

    # Μέθοδος που επιστρέφει τα φιλτρρισμένα προιόντα με διάφορες παραμέτρους
    def get_filtered_products(
        self,
        id=None,
        name=None,
        description=None,
        category=None,
        min_price=None,
        max_price=None,
        sort_by="id",
        order="asc"
    ):
        cursor = self.conn.cursor() # Δημιουργία cursor

        query = "SELECT * FROM products WHERE 1=1"  
        params = []

        # Προσθήκη φίλτρων στο query αν έχουν οριστεί τιμές
        if id is not None:
            query += " AND id = ?"
            params.append(id)
        if name:
            query += " AND name LIKE ?"
            params.append(f"%{name}%")
        if description:
            query += " AND description LIKE ?"
            params.append(f"%{description}%")    
        if category:
            query += " AND category = ?"
            params.append(category)
        if min_price is not None:
            query += " AND price >= ?"
            params.append(min_price)
        if max_price is not None:
            query += " AND price <= ?"
            params.append(max_price)

        # Επιτρέπεται μόνο τα συγκεκριμένα πεδία ταξινόμησης
        allowed_sort_fields = ["id", "name", "price", "category"]
        if sort_by not in allowed_sort_fields:
            sort_by = "id"

        # Προστασία για την κατεύθυνση ταξινόμησης
        if order not in ["asc", "desc"]:
            order = "asc"

        # Προσθήκη order by στο query
        query += f" ORDER BY {sort_by} {order.upper()}"

        cursor.execute(query, params)   # Εκτέλεση του query με τις παραμέτρους
        rows = cursor.fetchall()        # Ανακτησή όλων των αποτελεσμάτων

        # Μετατροπή των αποτελεσμάτων σε αντικείμενα Product
        return [Product.from_dict(dict(row)) for row in rows]

        
