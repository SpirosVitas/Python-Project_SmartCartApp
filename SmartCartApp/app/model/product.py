class Product:
    # Constructor: Αρχικοποιεί ένα νέο προϊόν με τις βασικές του ιδιότητες
    def __init__(self, id, name, description, category, price, image_url):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.price = price
        self.image_url = image_url

    # Έλεγχος ισότητας με id
    def __eq__(self,other):
        return self.id == other.id

    #Εμφάνιση με αυτή την σειρά    
    def __str__(self):
        return f"Product{self.id}: {self.name} - {self.description} - {self.category} - {self.price} - {self.image_url}"  

    #Εμφανιση και debugging
    def __repr__(self):
        return f"Product(id={self.id}, name={self.name}, description={self.description}, category={self.category}, price={self.price}, image_url={self.image_url})"

    #Μετροπή αντικειμένου σε dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "price": self.price,
            "image_url": self.image_url
        }
    
    #Δημιουργία αντικειμένου απο dictionary
    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            name=data.get("name"),
            description=data.get("description"),
            category=data.get("category"),
            price=data.get("price", 0.0),
            image_url=data.get("image_url")
        )
