from flask import jsonify, request  # Εισαγωγή βιβλιοθήκης για κλήσεις http και απαντήσεις
from app import server
from app.model.product import Product   # Εισαγωγή μοντέλο Product
from app.repositories.repository_product import ProductRepository   # Εισαγωγή Product Repository

prod_repo = ProductRepository()

# Δημιουργία route που δέχεται GET αιτήματα
@server.route('/products', methods=['GET']) 
def get_products():
    # Διαβάζει τις παραμέτρους απο το url 
    id = request.args.get('id', type=int)
    name = request.args.get('name', type=str)
    description = request.args.get('description', type=str)
    category = request.args.get('category', type=str)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', default='id', type=str)
    order = request.args.get('order', default='asc', type=str)

    # Καλέι την μέθοδο του repository για να πάρει τα προϊόντα με τα φίλτρα
    products = prod_repo.get_filtered_products(
        id=id,
        name=name,
        description=description,
        category=category,
        min_price=min_price,
        max_price=max_price,
        sort_by=sort_by,
        order=order
    )

    if not products:    # Αν δεν βρέθηκαν προϊόντα
        return jsonify({"message": "No available products"}), 404   # Επιστρέφει μήνυμα και status code 404

    # Επιστρέφει τη λίστα των προϊόντων σε μορφή Json
    return jsonify([product.to_dict() for product in products]), 200
    

