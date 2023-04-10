from decouple import config
from flask import Flask, render_template
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient(config("MONGO_DB"))
db = client["scrap"]
collection = db["scrap"]

@app.route('/')
def index():
    products = collection.find({"market":"saga", "web_dsct":{"$gte":90}, "date":"02/04/2023"})

    return render_template('product_grid.html', products=products)

if __name__ == '__main__':
    app.run()
