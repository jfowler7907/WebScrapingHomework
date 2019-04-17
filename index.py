from flask import Flask, render_template, redirect
import pymongo
import scrape_mars

app = Flask(__name__)

# setup mongo connection
conn = "mongodb://localhost:27017"
client = pymongo.MongoClient(conn)
db = client.mission_mars

@app.route("/")
def home():
    mars_info = db.collection.find_one()
    # Return template and datas
    return render_template("home.html", info=mars_info)

@app.route("/scrape")
def scrape():
    mars_info=scrape_mars.scrape()

    #Update the Mongo DB using update and insert=true
    db.collection.update({}, mars_info, upsert=True)

    # Redirect back to home page
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)