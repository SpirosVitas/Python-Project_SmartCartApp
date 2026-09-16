class CartItem:
    # Constructor: Αρχικοποιεί ένα νέο προϊόν με τις βασικές του ιδιότητες
    def __init__(self, product_id=None, product_name="", quantity=None, price=0.0):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity 
        self.price = price
    
    # Έλεγχος ισότητας με product_id
    def __eq__(self, other):
        return self.product_id == other.product_id
    
    #Εμφάνιση με αυτή την σειρά 
    def __str__(self):
        return f"CartItem({self.product_id}): {self.product_name} x {self.quantity} @ {self.price}"
    
    #Εμφανιση και debugging
    def __repr__(self):
        return (
            f"CartItem(product_id={self.product_id}, product_name={self.product_name}, quantity={self.quantity}, price={self.price})"
        )
    
    #Μετροπή αντικειμένου σε dictionary
    def to_dict(self):
        return{
            "product_id": self.product_id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "price": self.price
        }
    
    #Δημιουργία αντικειμένου απο dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data.get("product_id"),
            product_name=data.get("product_name"),
            quantity=data.get("quantity", 1),
            price=data.get("price", 0.0)
        )
