import time
from datetime import datetime


class Purchase:
    # Constructor: Αρχικοποιεί ένα νέο προϊόν με τις βασικές του ιδιότητες
    def __init__(self, id=None, created_at=None, total_price=0.0):
        self.id = id or self.generate_id()
        self.created_at = created_at or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.total_price = total_price

    #Δημιουργία Id με βάση το χρόνο
    def generate_id(self):
        return str(int(time.time()*1000))
      
    #Μετροπή αντικειμένου σε dictionary
    def to_dict(self):
        return{
            "id": self.id,
            "created_at": self.created_at,
            "total_price": self.total_price
        }    
    #Δημιουργία αντικειμένου απο dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            created_at=data.get("created_at"),
            total_price=data.get("total_price", 0.0)
        )
    
