import requests
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient




def base_link():

    client = MongoClient('mongodb://192.168.9.66:27017')
    db = client['oechsle']
    collection = db['links']

    data = collection.find({})
    list_url=[]
    for i in data:
        list_url.append(i["url"])

    


    for i,v in enumerate(list_url):

        # Your existing code to extract base_url
        response = requests.get(v)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            category = soup.find_all("script" )

            for i in category:
                if "/buscapagina?" in i.text:
                    pattern = re.compile(r'/buscapagina.*?PageNumber=')
                    match = pattern.search(i.text)
                    web = match.group()
                    base_url = "https://www.oechsle.pe" + web

            print()
            print(base_url)

            # Save base_url to MongoDB
            save_to_mongodb(v, base_url)

          

def save_to_mongodb(base, base_url):
    # Connect to MongoDB
    client = MongoClient('mongodb://192.168.9.66:27017')
    db = client['oechsle']
    collection = db['links']

    # Filter by "url": base
    filter_query = {"url": base}
    
    # Check if the document already exists
    existing_document = collection.find_one(filter_query)

    if existing_document:
        # Update the existing document with the new base_url
        collection.update_one(filter_query, {"$set": {"json_link": base_url}})
        print(f"Updated document for {base}")
    else:
        # Insert a new document
        new_document = {"url": base, "json_link": base_url}
        collection.insert_one(new_document)
        print(f"Inserted new document for {base}")

    # Close the MongoDB connection
    client.close()

# Example usage:
#ase_url = base_link("https://example.com")




base_link()