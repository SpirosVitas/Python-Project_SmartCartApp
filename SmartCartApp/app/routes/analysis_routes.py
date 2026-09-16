from flask import Flask, request, send_file, jsonify    # Εισαγωγή βιβλιοθήκης για κλήσεις http και απαντήσεις
from app import server
from matplotlib.figure import Figure
import matplotlib as plt    # Εισαγωγή βιβλιοθήκης για δημιουργία γραφημάτων
import numpy as np      # Εισαγωγή βιβλιοθήκης για υπολογισμούς
import sqlite3
from io import BytesIO  # Εισαγωγή βιβλιοθήκης για αποθήκευση στην μνήμη
from app.repositories.repository_analysis import AnalysisRepository # Εισαγωγή Analysis Repository

ana_repo = AnalysisRepository()

plt.use("agg")      # Για να τρέχουν τα διαγράμματα

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/analysis/top_products/chart", methods = ['GET'])
def top_products_chart():
    img = ana_repo.top_products_chart()         # Παίρνει την εικόνα από το repository
    return send_file(img, mimetype="image/png") # Επιστρέφει εικόνα png

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/analysis/top_products", methods = ['GET'])
def top_products():
    data = ana_repo.get_top_selling_products()  # Παίρνει τα δεδομένα από την βάση
    return jsonify([dict(row) for row in data]) # Τα επιστρέφει σε Json μορφή

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/analysis/top_products_per_category/chart", methods = ['GET'])
def top_products_per_category_chart():
    img = ana_repo.top_products_per_category_chart()    # Παίρνει την εικόνα από το repository
    return send_file(img, mimetype="image/png")         # Επιστρέφει εικόνα png

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/analysis/top_products_per_category", methods = ['GET'])
def top_products_by_category():
    data = ana_repo.top_products_per_category() # Παίρνει τα δεδομένα από την βάση
    return jsonify([dict(row) for row in data]) # Τα επιστρέφει σε Json μορφή

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/analysis/predict_sales", methods=['GET'])
def predict_sales_per_day():
    data = ana_repo.predict_daily_sales()   # Παίρνει τα δεδομένα από την βάση
    return jsonify(data)                    # Επιστρέφει τις προβλέψεις

# Δημιουργία route που δέχεται GET αιτήματα
@server.route("/analysis/predict_sales/chart", methods=['GET'])
def predict_sales_per_day_chart():
    img = ana_repo.daily_sales_prediction_chart()   # Παίρνει την εικόνα από το repository
    return send_file(img, mimetype="image/png")     # Επιστρέφει εικόνα png
