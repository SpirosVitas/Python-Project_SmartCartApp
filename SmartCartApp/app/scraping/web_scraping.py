import requests # Εισαγωγή βιβλιοθήκης για κλήσεις http 
from bs4 import BeautifulSoup   # Εισαγωγή βιβλιοθήκης για scraping

# Μέθοδος που κάνει το scraping 
def category_scraping(query, category):

    # Τα url στα οποία θα γίνει το scraping
    CATEGORY_URLS = {
        "smartphone": "https://justech.gr/index.php?route=product/category&path=1&limit=1000",
        "phone": "https://justech.gr/index.php?route=product/category&path=1&limit=1000",
        "tablet": "https://justech.gr/index.php?route=product/category&path=11&limit=1000",
        "smartwatch": "https://justech.gr/index.php?route=product/category&path=2&limit=1000",
        "camera": "https://justech.gr/index.php?route=product/category&path=5_17&limit=1000"
    }

    # Παίρνει το url για την συγκεκριμένη κατηγορία
    category_url = CATEGORY_URLS.get(category.lower())  # Κάνει την κατηγορία πεζά γράμματα
    
    if not category_url:    # Αν δεν βρεθεί κατηγορία, επιστρέφει σφάλμα
        return {"error": "Invalid category"}, 400
    
    response = requests.get(category_url)   # Κάνει το request στο site
    if response.status_code != 200: # Αν αποτύχει, επιστρέφει σφάλμα
        return {"error": "Failed to fetch data"}, 500
    
    # Γίνεται ανάλυσει του html από το site
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="content")   # Βρίσκει το id στο html
    item_elements = results.find_all("div", class_="product-thumb") #Βρίσκει το product-thumb που εκει είναι όλά τα προιόντα στο html
    query_lower = query.lower() #Μετατρέπει το query σε πεζά γραμματα

    # Για κάθε προιόν που βρίσκει
    for item_element in item_elements:
        try:
            name = item_element.find("div", class_="name").text.strip() # Παίρνει το όνομα
    
            if query_lower not in name.lower():
                continue    # Αν στο query δεν υπάρχει στο όνομα προχωράει στο επόμενο

            desc = item_element.find("div", class_="description").text.strip()      # Παίρνει τη περιγραφή
            price = item_element.find("div", class_="price").text.strip()           # Παίρνει την τιμή
            image_tag = item_element.find("img", class_="img-responsive img-first") # Παίρνει την εικόνα
            image_url = None

            if image_tag:
                srcset = image_tag.get("srcset", "")    # Παίρνει το srcset
                image_url = srcset.split(",")[-1].split()[0] if srcset else image_tag.get("src")    # Παίρνει την μεγαλύτερη εικόνα αλλιώς παίρνει το src

            # Επιστρέφει το πρώτο προϊόν
            return{
                "name": name,
                "description": desc,
                "price": price,
                "image_url": image_url
            }    
        
        except Exception as e:
            continue    # Αν κάποιο στοιχείο λείπει το αγνοεί και συνεχίζει 

    # Αν δεν βρεθεί κανένα προϊόν 
    return{"message": "No matching product found"}, 404    
