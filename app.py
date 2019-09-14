from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from scrape_mars import scrape

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars"
mongo = PyMongo(app)

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    mars_data = mongo.db.collection.find_one()
    return render_template("index.html", mars=mars_data)

@app.route("/scrape")
def scrape_route():    
    mars = scrape()
    mongo.db.collection.update({}, mars, upsert= True)

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)