###### CONTROL ######
config = "api/config.txt"
debug = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("debug") - 5]
mobile = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("mobile") - 5]
down = open(config).read().replace("\n", "")[open(config).read().replace("\n", "").index("down") - 5]
#-------------------#

from flask import Flask, request, render_template, send_file, Response, url_for, jsonify, redirect
import firebase_admin
from firebase_admin import credentials, firestore

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
    cred = credentials.Certificate("api/static/db/dbcache-507cd-firebase-adminsdk-srwcd-309135930e.json")
else:
    from api import main
    from api import pageGen
    from api import dashboard
    import os
    home = "https://powerscore.vercel.app"
    previews = "api/previews.json"
    cred = credentials.Certificate(json.loads(os.environ.get('db')))

###### INITIALIZE ######

db = firestore.client()
teamsDocRef = db.collection('kudos').document('ft1sudZqNNZhXjN9i7zO')

def getKudos(teamID):
    """Fetches the kudos data for a specific team ID."""
    doc = teamsDocRef.get()
    if doc.exists:
        data = doc.to_dict()
        print(f"Getting kudos count for team '{teamID}'.")
        return len(data.get(teamID, []))  # Return length of team's time strings array or empty if not present
    else:
        return TypeError

def addKudos(teamId, timeStamp):
    """Adds a kudos timestamp to a specific team ID in a Firestore document."""
    # Define the transaction update function using @firestore.transactional decorator
    @firestore.transactional
    def transactionUpdate(transaction):
        doc = teamsDocRef.get(transaction=transaction)
        if doc.exists:
            data = doc.to_dict()
            teamTimes = data.get(teamId, [])
            teamTimes.append(timeStamp)  # Add new timestamp to team's array
            transaction.update(teamsDocRef, {teamId: teamTimes})
        else:
            # If document doesn't exist, create it with the new team entry
            transaction.set(teamsDocRef, {teamId: [timeStamp]})
    
    try:
        transactionUpdate(db.transaction())  # Execute the transaction with the decorator
        print(f"Added kudos timestamp '{timeStamp}' for team '{teamId}'.")
    except Exception as e:
        print(f"An error occurred: {e}")

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
            return render_template("ranks.html", debug = debug, home = home, homeButton = homeButton, epochTime = time.time(), mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                                                                                 url_for('static', filename='/css/bottom-mobile.css'),
                                                                                                 url_for('static', filename='/css/ranks-mobile.css')])
        else:
            homeButton = "Back to Home"
            return render_template("ranks.html", debug = debug, home = home, homeButton = homeButton, epochTime = time.time(), mobile = [url_for('static', filename='/css/mainstyle.css'),
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
            return render_template("preferences.html", debug = debug, home = home, homeButton = homeButton, epochTime = time.time(), mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                                                                                 url_for('static', filename='/css/bottom-mobile.css'),
                                                                                                 url_for('static', filename='/css/ranks-mobile.css'),
                                                                                                 url_for('static', filename='/css/preference-mobile.css')])
        else:
            homeButton = "Back to Home"
            return render_template("preferences.html", debug = debug, home = home, homeButton = homeButton, epochTime = time.time(), mobile = [url_for('static', filename='/css/mainstyle.css'),
                                                                                                 url_for('static', filename='/css/bottom.css'),
                                                                                                 url_for('static', filename='/css/ranks.css'),
                                                                                                 url_for('static', filename='/css/preference.css')])

@app.route("/teams", methods=["GET"])
def handle_teams():
    global teamName
    if down == "Y":
        return render_template('down.html')
    else:
        print(request.args)
        query = request.args.get("query").upper()
        teamName = query
        season = request.args.get("season", default="190")
        try:
            result = main.runAlgorithm(query, season)
            IMAGE_URL = json.load(open(previews))["links"][str(round(result[1]))]
        except Exception as e:
            result = None
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
                                    home = home, homeButton = homeButton, name = query, epochTime = time.time(),
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
                                    home = home, homeButton = homeButton, name = query, epochTime = time.time(),
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
                    kudosCount = kudosCount, debug = debug, imageURL = f"https://powerscore.vercel.app/image-preview?team={result[0]}&ps={result[1]}&ops={result[4]}&dps={result[5]}", epochTime = time.time(),
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
                    kudosCount = kudosCount, debug = debug, imageURL = f"https://powerscore.vercel.app/image-preview?team={result[0]}&ps={result[1]}&ops={result[4]}&dps={result[5]}", epochTime = time.time(),
                    home = home, homeButton = homeButton) + dashboard.generateFrom(result[13])

@app.route("/competitions", methods=["GET"])
def handle_competitions():
    if down == "Y":
        return render_template('down.html')
    else:
        global excelFile, name, division
        print(request.args)
        query = request.args.get("query")
        division = request.args.get("division") or 1

        try:
            if "RE-V5RC" in query:
                query = query[query.index("RE-V5RC-"):query.index("RE-V5RC-") + 15]
            else:
                query = query[query.index("RE-VRC-"):query.index("RE-VRC-") + 14]
            
            if request.args.get("query") != query:
                return redirect(url_for("handle_competitions", query=query, division=division))
            
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
                                    home = home, homeButton = homeButton, epochTime = time.time(),
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
                                    home = home, homeButton = homeButton, epochTime = time.time(),
                                    mobile = [url_for('static', filename='/css/mainstyle.css'),
                                              url_for('static', filename='/css/bottom.css')])
        else:
            user_agent = request.headers.get('User-Agent').lower()
            if 'iphone' in user_agent or 'android' in user_agent or mobile == "Y":
                homeButton = "Home"
                htmlFile = render_template("comp.html", query = query, debug = debug, home = home, epochTime = time.time(), homeButton = homeButton, name = result[0], mobile = [url_for('static', filename='/css/mainstyle-mobile.css'),
                                                                                                        url_for('static', filename='/css/bottom-mobile.css'),
                                                                                                        url_for('static', filename='/css/comps-mobile.css')]) + pageGen.generateFrom(result, query, division, "", time=time.time())
            else:
                homeButton = "Back to Home"
                htmlFile = render_template("comp.html", query = query, debug = debug, home = home, epochTime = time.time(), homeButton = homeButton, name = result[0], mobile = [url_for('static', filename='/css/mainstyle.css'),
                                                                                                        url_for('static', filename='/css/bottom.css'),
                                                                                                        url_for('static', filename='/css/comps.css')]) + pageGen.generateFrom(result, query, division, "", time=time.time())
            return htmlFile


@app.route('/add-kudos', methods=['POST'])
def give_kudos():
    if down == "Y":
        return jsonify({"success": False})
    else:
        team = request.json['team']
        addKudos(team, time.time())

        return jsonify({"success": True})

@app.route('/get-kudos', methods=['POST'])
def get_kudos():
    if down == "Y":
        return jsonify({"success": False})
    else:
        team = request.json['team']
        kudos = getKudos(team)

        return jsonify({"success": True, "kudos": kudos})
        
@app.route("/download", methods=["GET"])
def download():
    if down == "Y":
        return render_template('down.html')
    else:
        return send_file(excelFile, as_attachment=True, download_name= name + "-division" + division + '.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route("/image-preview", methods=["GET"])
def image_preview():
    if down == "Y":
        return None
    else:
        team = request.args.get("team")
        ps = int(request.args.get("ps"))
        ops = int(request.args.get("ops"))
        dps = int(request.args.get("dps"))
        return Response(main.generateRichLinkPreview(team=team, ps=ps, ops=ops, dps=dps), mimetype='image/jpeg')


if debug == "Y":
    if __name__ == "__main__":
        app.run(debug=True)