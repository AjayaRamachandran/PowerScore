###### CONTROL ######
config = "api/config.txt"
debug = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("debug") - 5]
mobile = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("mobile") - 5]
down = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("down") - 5]
#-------------------#

from flask import Flask, request, render_template, send_file
import random
if debug == "Y":
    import main
    import pageGen
    import pageGenMobile
    import dashboard
else:
    from api import main
    from api import pageGen
    from api import pageGenMobile
    from api import dashboard

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
    if down == "Y":
        return render_template('down.html')
    else:
        user_agent = request.headers.get('User-Agent').lower()
        if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
            return render_template('splash-mobile.html')
        else:
            return render_template("splash.html", banner = img_tag, favicon = "")#base64.b64encode(open('favicon.ico', 'rb').read()).decode('utf-8'))

@app.route("/teams", methods=["GET"])
def handle_teams():
    if down == "Y":
        return render_template('down.html')
    else:
        query = request.args.get("query").upper()
        try:
            result = main.runAlgorithm(query)
        except Exception as e:
            result = None
            print(e)
        # Process the search query (e.g., query a database, perform a search, etc.)
        if result == None:
            user_agent = request.headers.get('User-Agent').lower()
            if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
                return render_template("oops-mobile.html",
                                    query = query,
                                    destination = "/teams",
                                    placeholder = "Search a Team Number",
                                    type = "team with the number",
                                    issue1 = "This team does not exist",
                                    issue2 = "This team exists but has not competed yet this season",
                                    issue3 = "RobotEvents API requests have timed out")
            else:
                return render_template("oops.html",
                                    query = query,
                                    destination = "/teams",
                                    placeholder = "Search a Team Number",
                                    type = "team with the number",
                                    issue1 = "This team does not exist",
                                    issue2 = "This team exists but has not competed yet this season",
                                    issue3 = "RobotEvents API requests have timed out")

        else:
            user_agent = request.headers.get('User-Agent').lower()
            if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
                return render_template("index-mobile.html",
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
                    barByteString = result[12]) + dashboard.generateFrom(result[13])
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
                    barByteString = result[12]) + dashboard.generateFrom(result[13])

@app.route("/competitions", methods=["GET"])
def handle_competitions():
    if down == "Y":
        return render_template('down.html')
    else:
        global excelFile, name, division
        query = request.args.get("query")
        division = request.args.get("division")
        try:
            result, excelFile = main.runComp(query, int(division) - 1)
            name = result[0]
        except Exception as e:
            result = None
            print(e)
        if result == None:
            user_agent = request.headers.get('User-Agent').lower()
            if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
                return render_template("oops-mobile.html",
                                    query = query,
                                    destination = "/competitions",
                                    placeholder = "Enter a Competition SKU (ex: RE-VRC-XX-XXXX)",
                                    type = "competition with the SKU",
                                    issue1 = "This competition does not exist",
                                    issue2 = "This competition has not happened yet",
                                    issue3 = "RobotEvents API requests have timed out")
            else:
                return render_template("oops.html",
                        query = query,
                        destination = "/competitions",
                        placeholder = "Enter a Competition SKU (ex: RE-VRC-XX-XXXX)",
                        type = "competition with the SKU",
                        issue1 = "This competition does not exist",
                        issue2 = "This competition has not happened yet",
                        issue3 = "RobotEvents API requests have timed out")
        else:
            user_agent = request.headers.get('User-Agent').lower()
            if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
                htmlFile = pageGenMobile.generateFrom(result, query, division, "")
            else:
                htmlFile = pageGen.generateFrom(result, query, division, "")
            return htmlFile
    
@app.route("/download", methods=["GET"])
def download():
    if down == "Y":
        return render_template('down.html')
    else:
        return send_file(excelFile, as_attachment=True, download_name= name + "-division" + division + '.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    app.run(debug=True)
    