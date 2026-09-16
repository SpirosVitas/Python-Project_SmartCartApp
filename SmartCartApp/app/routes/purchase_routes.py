from flask import request, jsonify  # Εισαγωγή βιβλιοθήκης για κλήσεις http και απαντήσεις
from app import server
from app.repositories.repository_cart_items import CartItemRepository   # Εισαγωγή CartItem Repository
from app.repositories.repository_purchase import PurchaseRepository     # Εισαγωγή Purchase Repository
from app.model.purchase import Purchase     # Εισαγωγή μοντέλου Purchase
from app.model.purchase_item import PurchaseItem    # Εισαγωγή μοντέλου PurchaseItem

cart_repo = CartItemRepository()
purchase_repo = PurchaseRepository()

# Δημιουργία route που δέχεται POST αιτήματα
@server.route("/purchase", methods=["POST"])
def complete_purchase():    # Ολοκλήρωση αγοράς
    cart_items = cart_repo.get_cart_items() # Παίρνει τα προϊόντα του καλαθιού
    if not cart_items:  # Αν το καλάθι είναι άδειο, επιστρέφει σφάλμα
        return jsonify({"error": "Cart is empty"}), 400

    total_price = sum(item.price * item.quantity for item in cart_items)    # Υπολογίζει συνολική τιμή
    purchase = Purchase(total_price=total_price)    # Δημιουργία αντικειμένου αγοράς

    purchase_items = [] # Δημιουργία λίστας για τα προϊόντα αγοράς
    for item in cart_items:
        purchase_items.append(  # Προσθήκη στον πίνακα
            PurchaseItem(   # Δημιουργία PurchaseItem για κάθε προϊόν
                purchase_id=purchase.id,
                product_id=item.product_id,
                product_name=item.product_name,
                quantity=item.quantity,
                price=item.price
            )
        )

    purchase_repo.create_purchase(purchase, purchase_items) # Καλεί την μέθοδο από το repository που αποθηκευει την αγορά
    cart_repo.clear_cart()  # Άδειασμα καλαθιού μετά την αγορά

    return jsonify({    
        "message": "Purchase completed successfully",   # Επιστροφή επιβεβαίωσης
        "purchase": purchase.to_dict(), # Επιστροφή πληροφοριών αγοράς σε μορφή Json
        "items": [item.to_dict() for item in purchase_items]    # Επιστρεφει τα αγορασμένα προιόντα μορφή Json
    }), 201

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/purchases", methods=["GET"])
def list_purchases():   # Επιστρέφει της αγορές
    purchases = purchase_repo.get_all_purchases()   # Παίρνει όλες τις αγορές από τη βάση
    return jsonify([purchase.to_dict() for purchase in purchases]), 200 # Επιστρέφει Json με όλες τις αγορές

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/purchases/<purchase_id>", methods=["GET"])
def purchase_details(purchase_id):  # Επιστρέφει τα προιόντα συγκεκριμένης αγοράς
    items = purchase_repo.get_purchase_items(purchase_id)   # Παίρνει προϊόντα από τη συγκεκριμένη αγορά
    if not items:
        return jsonify({"error": "Purchase not found"}), 404    # Αν δεν υπάρχουν, επιστρέφει σφάλμα
    return jsonify([item.to_dict() for item in items]), 200 # Επιστρέφει τα προϊόντα της αγοράς

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/purchases/items", methods=["GET"])
def list_all_purchase_items():  # Επιστρέφει όλα τα αγορασμένα προιόντα
    items = purchase_repo.get_all_purchase_items()  # Παίρνει όλα τα αγορασμένα προιόντα
    return jsonify([item.to_dict() for item in items]), 200 # Επιστρέφει σε μορφή Json όλα τα αγορασμένα προιόντα
