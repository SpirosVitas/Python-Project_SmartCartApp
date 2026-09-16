import sqlite3
import matplotlib.pyplot as plt     # Εισαγωγή βιβλιοθήκης για δημιουργία γραφημάτων
from matplotlib.figure import Figure
import numpy as np          # Εισαγωγή βιβλιοθήκης για υπολογισμούς
from io import BytesIO      # Εισαγωγή βιβλιοθήκης για αποθήκευση στην μνήμη
import pandas as pd         # Εισαγωγή βιβλιοθήκης για διαχείρηση dataframes
from sklearn.linear_model import LinearRegression   # Εισαγωγή βιβλιοθήκης για μοντέλο γραμμικής παλινδρόμησης
from sklearn import metrics     # Εισαγωγή βιβλιοθήκης για μετρικά
from sklearn.model_selection import train_test_split    # Εισαγωγή βιβλιοθήκης για  διαχωρισμό δεδομένων σε training και testing sets

class AnalysisRepository:
    # Constructor δημιουργεί σύνδεση με τη βάση δεδομένων
    def __init__(self, db_path = "smartcart.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row


    # Παίρνει τα πέντε προϊόντα με τις περισσότερες πωλήσεις 
    def get_top_selling_products(self, limit=5):
        cursor = self.conn.cursor()

        cursor.execute("""
                    SELECT product_name, SUM(quantity) as total_sales
                    FROM purchase_items
                    GROUP BY product_name
                    ORDER BY total_sales DESC
                    LIMIT ?
                    """, (limit,))
        return cursor.fetchall()
        

    # Δημιουργεί το διάγραμμα
    def top_products_chart(self, limit=5):  
        data = self.get_top_selling_products(limit) 

        products = [item["product_name"] for item in data]  # Παίνρει τα προιόντα
        sales = [item["total_sales"] for item in data]      # Παίρνει τις πωλήσεις

        fig = Figure(figsize=(10, 6))       # Δημιουργεί νέο γράφημα
        ax = fig.subplots()
        bars = ax.bar(products, sales)       # Δημιουργεί bar chart
        ax.set_title("Top 5 Best Selling Products")
        ax.set_xlabel("Product")
        ax.set_ylabel("Total Sales")

        for bar in bars:        # Εμφανίζει τις τιμές πάνω από κάθε μπάρα
            height = bar.get_height()
            ax.annotate(f'{height}', xy=(bar.get_x() + bar.get_width() / 2, height), 
                        xytext=(0, 3), textcoords="offset points", ha='center', fontsize=10)
        
        buf = BytesIO()     # Δημιουργεί buffer για την εικόνα
        fig.tight_layout()
        fig.savefig(buf, format="png")  # Αποθήκευει ως png
        plt.close()
        buf.seek(0)
        return buf      # Επιστρέφει την εικόνα
    

    # Παίρνει το προϊόν κάθε κατηγορίας με τις περισσότερες πωλήσεις
    def top_products_per_category(self):
        cursor = self.conn.cursor()

        cursor.execute( """
                     SELECT p.category, p.name, sum(pi.quantity) as total_sales 
                     FROM products p 
                     JOIN purchase_items pi on p.name = pi.product_name
                     GROUP BY p.category, p.name
                     HAVING total_sales = (
                       SELECT MAX(total_quantity)
                       FROM (
                        SELECT SUM(pi2.quantity) as total_quantity
                        FROM products p2
                        JOIN purchase_items pi2 on p2.name = pi2.product_name
                        WHERE p2.category = p.category
                        GROUP BY p2.name
                            ) 
                        )
                    """)
        return cursor.fetchall()
        
        

    # Δημιουργεί το διάγραμμα
    def top_products_per_category_chart(self):
        data = self.top_products_per_category()
        labels = [f"{item['category']}: {item['name']}" for item in data]
        values = [item["total_sales"] for item in data]
        fig =Figure(figsize=(10, 6))
        ax = fig.subplots()
        bars = ax.barh(labels, values, color="skyblue") # Δημιουργεί horizontal bar chart
        ax.set_xlabel("Total Sales")
        ax.set_title("Top Selling Product by Category")
    

        buf = BytesIO()     # Δημιουργεί buffer για την εικόνα
        fig.tight_layout()
        fig.savefig(buf, format="png")  # Αποθήκευει ως png
        plt.close()
        buf.seek(0)
        return buf      # Επιστρέφει την εικόνα


    # Φέρνει δεδομένα για παλινδρόμηση
    def get_regression_data(self):
        cursor = self.conn.cursor()
        cursor.execute("""
                    SELECT pi.quantity, p.category, strftime('%w', pur.created_at) AS day_of_week
                    FROM purchase_items pi 
                    JOIN products p ON pi.product_id = p.id
                    JOIN purchases pur ON pi.purchase_id = pur.id
                    """)
        rows = cursor.fetchall()
        return pd.DataFrame(rows, columns=["quantity", "category", "day_of_week"])  # Τα βάζει σε dataframe


    def predict_daily_sales(self):
        df = self.get_regression_data() # Παίρνει τα δεδομένα

        df["day_of_week"] = df["day_of_week"].astype(int)   # Μετατρέπει του τύπους
        df["quantity"] = df["quantity"].astype(int)
        df["category"] = df["category"].astype(str)

        df_grouped = df.groupby(["category", "day_of_week"])["quantity"].sum().reset_index() # Κάνει Sum και group by στα δεδομένα

        results = {}    # Αποθηκεύει τα αποτελέσματα

        for category in df_grouped["category"].unique():    # Για κάθε κατηγορία
            cat_data = df_grouped[df_grouped["category"] == category]   # Φιλτράρει τα δεδομένα της κατηγορίας

            X = cat_data[["day_of_week"]]   # Ημέρα ανεξάρτητη μεταβλητή
            Y = cat_data[["quantity"]]      # Ποσότητα εξαρτημένη μεταβλητή

            # Χωρίζει τα δεδομένα για train και test
            X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

            model = LinearRegression()  # Δημιουργεί γραμμικό μοντέλο
            model.fit(X,Y)              # Εκπαίδευει το μοντέλο


            days = pd.DataFrame({"day_of_week": list(range(7))})    # Δημιουργεί ημέρες 0-6
            predictions = model.predict(days)       # Κάνει πρόβλεψη για κάθε μέρα

            # Προβλέπει τις πωλήσεις για κάθε μέρα και υπολογίζει το μέσο τετραγωνικό σφάλμα
            results[category] = {
                "predictions": {str(day): round(float(pred), 2) for day, pred in zip(days["day_of_week"], predictions)},
                    "mse": round(float(metrics.mean_squared_error(Y_test, model.predict(X_test))), 2)
            }

        return results    


    def daily_sales_prediction_chart(self):
        df = self.get_regression_data()
        df["day_of_week"] = df["day_of_week"].astype(int)
        df["quantity"] = df["quantity"].astype(int)
        df["category"] = df["category"].astype(str)

        df_grouped = df.groupby(["category", "day_of_week"])["quantity"].sum().reset_index()

        categories = df_grouped["category"].unique()
        # Δημιουργεί γραφήματα για κάθε κατηγορία
        fig, axs = plt.subplots(len(categories), 1, figsize=(10, 3 * len(categories)), sharex=True)


        # Βάζει τα δεδομένα στα γραφήματα
        for ax, category in zip(axs, df_grouped["category"].unique()):
            cat_data = df_grouped[df_grouped["category"] == category]
            X = cat_data[["day_of_week"]]
            Y = cat_data["quantity"]

            model = LinearRegression()
            model.fit(X, Y)


            days = pd.DataFrame({"day_of_week": list(range(7))})
            predictions = model.predict(days)

            ax.scatter(X, Y, color='blue', label="Sales")   # Βάζει τα σημέια
            ax.plot(days["day_of_week"], predictions, color='red', label="Regression Line") # Βάζει τη γραμμή 
            ax.set_title(f"{category}")
            ax.set_ylabel("Sales")
            ax.legend()
            ax.grid(True)

        axs[-1].set_xlabel("Day of Week (0=Sun, ..., 6=Sat)")   # Ετικέτα με τις ημέρες

        buf = BytesIO()     # Δημιουργεί buffer για την εικόνα
        fig.tight_layout()
        fig.savefig(buf, format="png")      # Αποθήκευει ως png
        plt.close()
        buf.seek(0)
        return buf          # Επιστρέφει την εικόνα
