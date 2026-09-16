import time

class PurchaseItem:
    # Constructor: Αρχικοποιεί ένα νέο προϊόν με τις βασικές του ιδιότητες
    def __init__(self, id=None, purchase_id=None, product_id=None, product_name="", quantity=None, price=0.0):
        self.id = id or self.generate_id()
        self.purchase_id = purchase_id
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.price = price

    #Δημιουργία Id με βάση το χρόνο
    def generate_id(self):
        return str(int(time.time()*1000))

    #Μετροπή αντικειμένου σε dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "purchase_id": self.purchase_id,
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price
        }

    #Δημιουργία αντικειμένου απο dictionary    
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            purchase_id=data.get("purchase_id"),
            product_id=data.get("product_id"),
            product_name=data.get("product_name"),
            quantity=data.get("quantity"),
            price=data.get("price")
        )
