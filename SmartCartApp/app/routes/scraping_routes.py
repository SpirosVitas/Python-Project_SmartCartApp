from flask import request, jsonify  # Εισαγωγή βιβλιοθήκης για κλήσεις http και απαντήσεις
from app import server
from app.scraping.web_scraping import category_scraping # Εισαγωγή category scraping

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/scraping", methods=["GET"])
def products_scraping():    # Κάνει το scraping
    # Παίρνει τις παραμέτρους από το url
    query = request.args.get("product")
    category = request.args.get("category")

    # Αν λείπει το όνομα ή η κατηγορία επιστρέφει σφάλμα
    if not query or not category:
        return jsonify({"error": "Missing product or category"}), 400
    
    result = category_scraping(query, category) # Καλεί την μέθοδο που κάνει το scraping 
    if not result:  # Αν δεν βρεί το προιόν επιστρέφει μήνυμα
        return jsonify({"message": "No product found"}), 404
    
    return jsonify(result), 200 # Επιστρέφει τα δεδομένα
