from flask import request, jsonify # Εισαγωγή βιβλιοθήκης για κλήσεις http και απαντήσεις
from app import server
from app.model.cart_item import CartItem    # Εισαγωγή μοντέλου CartItem
from app.repositories.repository_cart_items import CartItemRepository  # Εισαγωγή CartItem Repository
from app.repositories.repository_product import ProductRepository   # Εισαγωγή Product Repository


cart_repo = CartItemRepository()
prod_repo = ProductRepository()

# Δημιουργία route που δέχεται POST αιτήματα
@server.route('/cart', methods=['POST'])
def add_to_basket():    # Προσθέτει στο καλάθι
    data = request.get_json()   # Παίρνει τα δεδομένα του αιτήματος σε JSON μορφή
    product_id = data.get('product_id')
    product_name = data.get('product_name')
    quantity = data.get('quantity')
    
     # Ελέγχει αν η ποσότητα είναι έγκυρη
    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({"error": "Invalid quantity"}), 400
    
    product = None # Αρχικοποιεί την μεταβλητή προιόνοτος

    if product_id:  # Αν δόθηκε product_id
        products = prod_repo.get_filtered_products(id=product_id)
        if products:
            product = products[0]  # Επιλέγει το πρώτο προιόν
    elif product_name:  # Αν όχι, αλλά δόθηκε όνομα
        products = prod_repo.get_filtered_products(name=product_name)
        if products:
            product = products[0]

    if not product: # Αν δεν βρέθηκε προϊόν
        return jsonify({"error": "Product not found"}), 404        
    
    # Δημιουργία αντικειμένου καλαθιού
    item = CartItem(
        product_id=product.id,
        product_name=product.name,
        quantity=quantity,
        price=product.price
    )
    cart_repo.add_to_cart(item) # Καλεί την μέθοδο από το repository που κάνει προσθήκη στο καλάθι


    # Επιστρέφει επιβεβαίωση , item και status code 201
    return jsonify({
        "message": "Product added to cart.",
        "item": item.to_dict()
    }), 201

# Δημιουργία route που δέχεται GET αιτήματα
@server.route('/cart', methods=['GET']) 
def get_basket(): # Επιστρέφει το καλάθι
    items = cart_repo.get_cart_items()  # Παίρνει όλα τα προϊόντα στο καλάθι
    if not items:   # Αν είναι άδειο
        return jsonify({"message": "Empty cart"}), 200   

    return jsonify([item.to_dict() for item in items]), 200 # Επιστρέφει τα προιόντα του καλαθιού σε μορφή Json


# Δημιουργία route που δέχεται PUT αιτήματα
@server.route('/cart', methods=['PUT'])
def update_item_quantity(): #Ενημερώνει την ποσότητα
    data = request.get_json()
    product_id = data.get("product_id")
    product_name = data.get("product_name")
    quantity = data.get("quantity")

    # Ελέγχει αν η ποσότητα είναι έγκυρη
    if not isinstance(quantity, int) or quantity < 1:
        return jsonify({"error": "Invalid quantity, must be integer"}), 400
    
    if not product_id and product_name: # Αν δεν δόθηκε ID αλλά όνομα
        products = prod_repo.get_filtered_products(name=product_name)
        if products:
            product_id = products[0].id

    if not product_id:  # Αν δεν δόθηκε ID ή όνομα
        return jsonify({"error": "product_id or product_name required"}), 400        

    success = cart_repo.update_quantity(product_id, quantity)   # Αν το προιόν βρίσκεται στο καλάθι
    if not success: # Αν δεν βρίσκεται
        return jsonify({"error": "Product not in cart"}), 404

    return jsonify({"message": "Quantity updated"}), 200

# Δημιουργία route που δέχεται DELETE αιτήματα
@server.route('/cart/item', methods=['DELETE'])
def remove_item():  # Διαγραφή από το καλάθι

    # Διαβάζει τις παραμέτρους απο το url 
    product_id = request.args.get('product_id', type=int)
    product_name = request.args.get('product_name')

    if not product_id and product_name: # Αν δόθηκε το όνομα
        products = prod_repo.get_filtered_products(name=product_name)
        if products:
            product_id = products[0].id
    
    if not product_id: # Αν δεν βρέθηκε το ID
        return jsonify({"error": "Missing product_id or product_name"}), 404
    
    deleted = cart_repo.remove_from_cart(product_id) # Αν το προιόν βρίσκεται στο καλάθι
    if not deleted:# Αν δεν βρίσκεται
        return jsonify({"error": "Product not in cart"}), 404

    return jsonify({"message": "Product removed"}), 200


# Δημιουργία route που δέχεται DELETE αιτήματα
@server.route('/cart', methods=['DELETE'])
def clear_the_cart():   # Διαγρφή καλαθιού
    cart_repo.clear_cart()
    return jsonify({"message": "Cart deleted"}), 200

