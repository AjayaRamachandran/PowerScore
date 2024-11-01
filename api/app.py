###### CONTROL ######
config = "api/config.txt"
debug = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("debug") - 5]
mobile = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("mobile") - 5]
down = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("down") - 5]
#-------------------#

from flask import Flask, request, render_template, send_file, url_for, jsonify, redirect
import time
import requests
import json

if debug == "Y":
    import main
    import pageGen
    import dashboard
    import osEmul as os
    home = "http://localhost:5000"
    previews = "api/previews.json"
else:
    from api import main
    from api import pageGen
    from api import dashboard
    import os
    home = "https://powerscore.vercel.app"
    previews = "api/previews.json"

###### INITIALIZE ######
PANTRY_KEY = os.environ.get("db")
#KUDOS_FILE_PATH = '/kudos.json'

def apiAction(action, endpoint = "", params = None, data = None):
        headers = {
            'Content-Type': 'application/json'
        }

        BASE_URL = f'{PANTRY_KEY}'

        if action == "get":
            try:
                response = requests.get(f'{BASE_URL}{endpoint}', headers=headers, params=params)
                print(f"Kudos: {response}")
                return response.json()
            except Exception as e:
                print(e)
                return None
        elif action == "post":
            try:
                requests.post(f'{BASE_URL}{endpoint}', json=data)
            except Exception as e:
                print(e)



###### WEBAPP ######
app = Flask(__name__)

@app.route("/")
def index():
    if down == "Y":
        return render_template('down.html')
    else:
        user_agent = request.headers.get('User-Agent').lower()
        if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
            return render_template('splash-mobile.html', debug = debug)
        else:
            return render_template("splash.html", debug = debug)

@app.route("/ranks", methods=["GET"])
def ranks():
    if down == "Y":
        return render_template('down.html')
    else:
        user_agent = request.headers.get('User-Agent').lower()
        if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
            homeButton = "Home"
            return render_template("ranks.html", debug = debug, home = home, homeButton = homeButton, mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                                                                                 url_for('static', filename='/css/bottom-mobile.css'),
                                                                                                 url_for('static', filename='/css/ranks-mobile.css')])
        else:
            homeButton = "Back to Home"
            return render_template("ranks.html", debug = debug, home = home, homeButton = homeButton, mobile = [url_for('static', filename='/css/mainstyle.css'),
                                                                                                 url_for('static', filename='/css/bottom.css'),
                                                                                                 url_for('static', filename='/css/ranks.css')])

@app.route("/preferences", methods=["GET"])
def preferences():
    if down == "Y":
        return render_template('down.html')
    else:
        user_agent = request.headers.get('User-Agent').lower()
        if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
            homeButton = "Home"
            return render_template("preferences.html", debug = debug, home = home, homeButton = homeButton, mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                                                                                 url_for('static', filename='/css/bottom-mobile.css'),
                                                                                                 url_for('static', filename='/css/ranks-mobile.css'),
                                                                                                 url_for('static', filename='/css/preference-mobile.css')])
        else:
            homeButton = "Back to Home"
            return render_template("preferences.html", debug = debug, home = home, homeButton = homeButton, mobile = [url_for('static', filename='/css/mainstyle.css'),
                                                                                                 url_for('static', filename='/css/bottom.css'),
                                                                                                 url_for('static', filename='/css/ranks.css'),
                                                                                                 url_for('static', filename='/css/preference.css')])

@app.route("/teams", methods=["GET"])
def handle_teams():
    global teamName
    if down == "Y":
        return render_template('down.html')
    else:
        query = request.args.get("query").upper()
        teamName = query
        season = request.args.get("season", default="190")
        try:
            result = main.runAlgorithm(query, season)
            IMAGE_URL = json.load(open(previews))["links"][str(round(result[1]))]
        except Exception as e:
            result = None
            print(e)
        # retrieves kudos count
        kudos_data = apiAction("get")

        # Append new kudos entry
        try:
            kudosCount = len(kudos_data["kudos"][query])
        except Exception as e:
            print(e)
            kudosCount = 0

        # Process the search query (e.g., query a database, perform a search, etc.)
        if result == None:
            user_agent = request.headers.get('User-Agent').lower()
            if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
                homeButton = "Home"
                return render_template("oops-team.html", debug = debug, 
                                    query = query,
                                    destination = "/teams",
                                    placeholder = "Search a Team Number",
                                    type = "team with the number",
                                    issue1 = "This team does not exist",
                                    issue2 = "This team exists but has not competed yet this season",
                                    issue3 = "RobotEvents API requests have timed out",
                                    home = home, homeButton = homeButton, name = query,
                                    mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                              url_for('static', filename='/css/bottom-mobile.css'),
                                              url_for('static', filename='/css/comps-mobile.css')])
            else:
                homeButton = "Back to Home"
                return render_template("oops-team.html",
                                    query = query, debug = debug, 
                                    destination = "/teams",
                                    placeholder = "Search a Team Number",
                                    type = "team with the number",
                                    issue1 = "This team does not exist",
                                    issue2 = "This team exists but has not competed yet this season",
                                    issue3 = "RobotEvents API requests have timed out",
                                    home = home, homeButton = homeButton, name = query,
                                    mobile = [url_for('static', filename='/css/mainstyle.css'),
                                              url_for('static', filename='/css/bottom.css'),
                                              url_for('static', filename='/css/comps.css')])

        else:
            user_agent = request.headers.get('User-Agent').lower()
            if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
                homeButton = "Home"
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
                    barByteString = result[12], arrowColor = result[14], arrowSvg = result[15],
                    kudosCount = kudosCount, debug = debug, imageURL = IMAGE_URL,
                    home = home, homeButton = homeButton) + dashboard.generateFrom(result[13])
            else:
                homeButton = "Back to Home"
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
                    barByteString = result[12], arrowColor = result[14], arrowSvg = result[15],
                    kudosCount = kudosCount, debug = debug, imageURL = IMAGE_URL,
                    home = home, homeButton = homeButton) + dashboard.generateFrom(result[13])

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
                homeButton = "Home"
                return render_template("oops.html",
                                    query = query, debug = debug, 
                                    destination = "/competitions",
                                    placeholder = "Enter a Competition SKU (ex: RE-VRC-XX-XXXX)",
                                    type = "competition with the SKU",
                                    issue1 = "This competition does not exist",
                                    issue2 = "This competition has not happened yet",
                                    issue3 = "RobotEvents API requests have timed out",
                                    home = home, homeButton = homeButton,
                                    mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                              url_for('static', filename='/css/bottom-mobile.css')])
            else:
                homeButton = "Back to Home"
                return render_template("oops.html",
                                    query = query, debug = debug, 
                                    destination = "/competitions",
                                    placeholder = "Enter a Competition SKU (ex: RE-VRC-XX-XXXX)",
                                    type = "competition with the SKU",
                                    issue1 = "This competition does not exist",
                                    issue2 = "This competition has not happened yet",
                                    issue3 = "RobotEvents API requests have timed out",
                                    home = home, homeButton = homeButton,
                                    mobile = [url_for('static', filename='/css/mainstyle.css'),
                                              url_for('static', filename='/css/bottom.css')])
        else:
            user_agent = request.headers.get('User-Agent').lower()
            if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
                homeButton = "Home"
                htmlFile = render_template("comp.html", debug = debug, home = home, homeButton = homeButton, name = result[0], mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                                                                                        url_for('static', filename='/css/bottom-mobile.css'),
                                                                                                        url_for('static', filename='/css/comps-mobile.css')]) + pageGen.generateFrom(result, query, division, "")
            else:
                homeButton = "Back to Home"
                htmlFile = render_template("comp.html", debug = debug, home = home, homeButton = homeButton, name = result[0], mobile = [url_for('static', filename='/css/mainstyle.css'),
                                                                                                        url_for('static', filename='/css/bottom.css'),
                                                                                                        url_for('static', filename='/css/comps.css')]) + pageGen.generateFrom(result, query, division, "")
            return htmlFile


@app.route('/give-kudos', methods=['POST'])
def give_kudos():
    if down == "Y":
        return jsonify({"success": False})
    else:
        team = request.json['team']
        kudos_data = apiAction("get")
        # Append new kudos entry
        try:
            kudos_data["kudos"][team].append({"time": time.time()})
        except Exception as e:
            print(e)
            kudos_data["kudos"][team] = []
            kudos_data["kudos"][team].append({"time": time.time()})

        # Upload the updated kudos file
        apiAction("post", data=kudos_data)
        return jsonify({"success": True})

@app.route("/download", methods=["GET"])
def download():
    if down == "Y":
        return render_template('down.html')
    else:
        return send_file(excelFile, as_attachment=True, download_name= name + "-division" + division + '.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    app.run(debug=True)
    