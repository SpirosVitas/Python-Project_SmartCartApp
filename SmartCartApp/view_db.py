import sqlite3

conn = sqlite3.connect("smartcart.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM products")
rows = cursor.fetchall()

for row in rows:
    print(row)
    print()

conn.close()
