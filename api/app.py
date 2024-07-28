###### CONTROL ######
config = "api/config.txt"
debug = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("debug") - 5]
mobile = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("mobile") - 5]
down = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("down") - 5]
#-------------------#

from flask import Flask, request, render_template, send_file, url_for, jsonify, redirect
import json
import dropbox
import time
import requests

if debug == "Y":
    import main
    import pageGen
    import dashboard
    import osEmul as os
    home = "http://localhost:5000"
else:
    from api import main
    from api import pageGen
    from api import dashboard
    import os
    home = "https://powerscore.vercel.app"

###### INITIALIZE ######
PANTRY_KEY = os.environ.get("pantry")
#KUDOS_FILE_PATH = '/kudos.json'

def apiAction(action, endpoint = "", params = None, data = None):
        headers = {
            'Content-Type': 'application/json'
        }

        BASE_URL = f'https://getpantry.cloud/apiv1/pantry/{PANTRY_KEY}/basket/powerscore'

        if action == "get":
            response = requests.get(f'{BASE_URL}{endpoint}', headers=headers, params=params)
            print(response)
            return response.json()
        elif action == "post":
            requests.post(f'{BASE_URL}{endpoint}', json=data)



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
            return render_template("splash.html")

@app.route("/ranks", methods=["GET"])
def ranks():
    if down == "Y":
        return render_template('down.html')
    else:
        user_agent = request.headers.get('User-Agent').lower()
        if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
            homeButton = "Home"
            return render_template("ranks.html", home = home, homeButton = homeButton, mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                                                                                 url_for('static', filename='/css/bottom-mobile.css'),
                                                                                                 url_for('static', filename='/css/ranks-mobile.css')])
        else:
            homeButton = "Back to Home"
            return render_template("ranks.html", home = home, homeButton = homeButton, mobile = [url_for('static', filename='/css/mainstyle.css'),
                                                                                                 url_for('static', filename='/css/bottom.css'),
                                                                                                 url_for('static', filename='/css/ranks.css')])


@app.route("/teams", methods=["GET"])
def handle_teams():
    global teamName
    if down == "Y":
        return render_template('down.html')
    else:
        query = request.args.get("query").upper()
        teamName = query
        season = request.args.get("season", default="181")
        try:
            result = main.runAlgorithm(query, season)
        except Exception as e:
            result = None
            print(e)

        # retrieves kudos count
        kudos_data = apiAction("get")

        # Append new kudos entry
        try:
            kudosCount = len(kudos_data["kudos"][query])
        except:
            kudosCount = 0

        # Process the search query (e.g., query a database, perform a search, etc.)
        if result == None:
            user_agent = request.headers.get('User-Agent').lower()
            if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
                homeButton = "Home"
                return render_template("oops-team.html",
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
                                    query = query,
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
                    barByteString = result[12], kudosCount = kudosCount,
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
                    barByteString = result[12], kudosCount = kudosCount,
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
                                    query = query,
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
                                    query = query,
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
                htmlFile = render_template("comp.html", home = home, homeButton = homeButton, mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                                                                                        url_for('static', filename='/css/bottom-mobile.css'),
                                                                                                        url_for('static', filename='/css/comps-mobile.css')]) + pageGen.generateFrom(result, query, division, "")
            else:
                homeButton = "Back to Home"
                htmlFile = render_template("comp.html", home = home, homeButton = homeButton, mobile = [url_for('static', filename='/css/mainstyle.css'),
                                                                                                        url_for('static', filename='/css/bottom.css'),
                                                                                                        url_for('static', filename='/css/comps.css')]) + pageGen.generateFrom(result, query, division, "")
            return htmlFile


@app.route('/give-kudos', methods=['GET'])
def give_kudos():
    if down == "Y":
        return jsonify({"success": False})
    else:
        team = request.args.get("team")
        kudos_data = apiAction("get")
        # Append new kudos entry
        try:
            kudos_data["kudos"][team].append({"time": time.time()})
        except:
            kudos_data["kudos"][team] = []
            kudos_data["kudos"][team].append({"time": time.time()})

        # Upload the updated kudos file
        apiAction("post", data=kudos_data)
        return redirect(url_for('handle_teams', query = team))

@app.route("/download", methods=["GET"])
def download():
    if down == "Y":
        return render_template('down.html')
    else:
        return send_file(excelFile, as_attachment=True, download_name= name + "-division" + division + '.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

if __name__ == "__main__":
    app.run(debug=True)
    