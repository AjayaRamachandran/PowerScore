from flask import Flask, request, render_template
import random
import main
import base64

###### BANNER ######
# Read the image file
image_data = open('Banner.jpg', 'rb').read()

# Encode as base64
data_uri = base64.b64encode(image_data).decode('utf-8')

# Create an <img> tag with the base64-encoded image
img_tag = data_uri

###### WEBAPP ######
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("splash.html", banner = img_tag)

@app.route("/search", methods=["GET"])
def handle_search():
    query = request.args.get("query")
    try:
        result = main.runAlgorithm(query)
    except Exception as e:
        result = None
        print(e)
    # Process the search query (e.g., query a database, perform a search, etc.)
    if result == None:
        return render_template("oops.html", query = query)
    else:
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
            graphByteString = result[10],
            xpLeft = result[11],
            barByteString = result[12])

if __name__ == "__main__":
    app.run(debug=True)