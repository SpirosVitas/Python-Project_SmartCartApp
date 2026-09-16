import sqlite3

def view_all_data(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Πάρε τα ονόματα των πινάκων
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    for table_name in tables:
        print(f"\n📦 Περιεχόμενα πίνακα: {table_name[0]}")
        cursor.execute(f"SELECT * FROM {table_name[0]}")
        rows = cursor.fetchall()
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    view_all_data("smartcart.db")
