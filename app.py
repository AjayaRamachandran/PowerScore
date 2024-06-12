from flask import Flask, request, render_template
import random
import main

app = Flask(__name__)

@app.route("/")
def index():
    return render_template(
        "index.html",
        powerscore = str(random.randint(1,100)),
        old_powerscore = str(random.randint(1,100)),
        rank = "Diamond II",
        offensive_powerscore = str(random.randint(1,100)),
        defensive_powerscore = str(random.randint(1,100)),
        title = "Sentinel",
        accolade1 = ["Top Fragger", "Attain the Highest Powerscore at a competition"],
        accolade2 = ["Started From the Bottom", "Climb from below Gold to above Platinum in a season"],
        badgeByteString = None,
        graphByteString = None)

@app.route("/search", methods=["GET"])
def handle_search():
    query = request.args.get("query")
    result = main.runAlgorithm(query)
    # Process the search query (e.g., query a database, perform a search, etc.)
    return render_template("index.html",
        name = result[0],
        powerscore = result[1],
        old_powerscore = result[2],
        rank = result[3],
        offensive_powerscore = result[4],
        defensive_powerscore = result[5],
        title = result[6],
        accolade1 = result[7],
        accolade2 = result[8],
        badgeByteString = result[9],
        graphByteString = None)

if __name__ == "__main__":
    app.run(debug=True)