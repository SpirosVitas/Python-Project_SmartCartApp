from flask import Flask, request, jsonify   # Εισαγωγή βιβλιοθήκης για κλήσεις http και απαντήσεις
from app import server
from app.repositories.ai_repository import AIRepository # Εισαγωγή AI Repository

ai_repo = AIRepository()

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/ai/evaluate", methods=['GET'])
def evaluate_cart():    # Αξιολογεί το καλάθι
    try:
        cart_items, response = ai_repo.rate_cart()  # Καλεί τη μέθοδο από το repository που αξιολογεί το καλάθι

        if cart_items is None:  # Αν το καλάθι είναι άδειο
            return jsonify({"error": response}), 400    # Επιστρέφει μήνυμα λάθους
        
        # Επιστρέφει το καλάθι και την αξιολόγηση σε μορφή Json
        return jsonify({
            "cart": cart_items,
            "evaluation": response
        })
    # Αν κάτι σπάσει επιστρέφει σφάλμα
    except Exception as e:
        return jsonify({"error": str(e)}), 500
