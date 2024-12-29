<p align="center">
<img src="https://www.dropbox.com/scl/fi/jk33040qbewi0lqfs1tbe/PS2.png?rlkey=75wqlp7ptpr9n6koeoi6ew73w&st=dequz2hg&raw=1" width="150" height ="150">
<h1 align="center">PowerScore on VRC-Tracker</h1>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-navy?logo=python"> <img src="https://img.shields.io/badge/JavaScript-yellow?logo=javascript"> <img src="https://img.shields.io/badge/HTML-orange?logo=html5">  *  <img src="https://img.shields.io/badge/Vercel-black?logo=Vercel"> <img src="https://img.shields.io/badge/Flask-gray?logo=flask">
</p>

## VRC-Tracker: A Flask Web Application on Vercel

<b>[VRC-Tracker](https://powerscore.vercel.app/)</b> is a HTML/CSS/JS webapp built using the [Flask](https://flask.palletsprojects.com/en/3.0.x/) framework, to connect a robust frontend with a powerful backend. The program receives regular support to this day, with new features and maintenance updates rolled out mostly weekly. The Flask WSGI internally uses [Werkzeug](https://werkzeug.palletsprojects.com/en/3.0.x/) and [Jinja](https://jinja.palletsprojects.com/en/3.1.x/). This application is designed to work without the need for server-side file storage, so that it may be deployed on any service. To download and run it locally, download this repository, change "Debug" to "Y" in `config.txt` and run `app.py` on your local machine; the application will be available on your localhost (port `5000` by default).

### Server-side requirements (for running locally)
VRC-Tracker makes frequent requests to the <b>[RobotEvents API](https://www.robotevents.com/api/v2)</b>. This means you will need a stable internet connection. If you are planning on running the program locally, go to the RobotEvents API site and get a set of API keys to use. Create a file in the `api` folder called "osEmul.py" setup as shown below:
```python
class environ():
    def __init__():
        None
    def get(key):
        apiKeys = {
            "API_KEY1" : "Enter Key Here!"
            # add more api keys here
            }
        return apiKeys[key]
```
Keep in mind that the `kudos` functionality will not be available by default on your local machine. If no action is taken, all `kudos` counts will simply display as 0 - if you wish, you may connect a Firebase Firestore database to your installation by placing your authentication .JSON file inside of `Root > api > static > db`

---
### What is the PowerScore Algorithm?
In VEX Robotics, teams play to compete for high points while trying to keep their opponents from doing the same thing. Games are set up by "alliances", which are randomly assigned pairs of teams that oppose a different pair of teams. Since individual statistics of a team in a match are not tracked in VEX Robotics, it can be difficult to determine how one team contributes to the outcome of their game. This knowledge is important for picking the correct partner in the elimination phase of the tournament. Thus, algorithms like OPR/DPR/CCWM, AdamScore, TrueSkill, and others have tried to calculate this "individual contribution", but each one has its own drawbacks. Powerscore has been rated the most accurate to a team's actual skill by numerous VEX robotics participants, and places amongst the very best algoriths after using the [Forward Predictive Test](https://en.wikipedia.org/wiki/Validity_(statistics)#:~:text=on%20performance%20reviews.-,Predictive%20validity,-%5Bedit%5D). Here's how it works.

Synopsis: The PowerScore algorithm is an advanced team evaluation algorithm that takes into account a team's ability to bring its own alliance to victory, as well as analyze how efficiently a team shuts its opponents down. The algorithm is multilayered and makes use of many different mathematical functions to work. The end result is a scale of localized values that represent the varying levels of match "power" shown by teams at a VEX Robotics Competition.

#### Elements of the Algorithm
Powerscore makes frequent use of the value named `matchDiff`. Put simply, it is the difference in score between a team and their opponent for a single match. Match diffs often vary, but we can establish an axiom to work off of. Namely, that as a team plays many matches, outside factors become less relevant toward establishing a relationship between the true skill differential of teams in a match and their respective match diffs. If we accept this axiom to be true, given the fact that it bears many similarities to the Central Limit Theorem, a lot of data can be extrapolated from it.

A team may average a match diff of `+30` across all their games. In other words, on average they win by 30 points. If in one randomly selected match they lose by, say, 20 points (having a match diff of `-20`), we can reasonably assume one of three things has occured.

> 1. The team's alliance partner was significantly worse than the average alliance partner for our team.
> 2. The team's opponent was significantly better than the average opponent for our team.
> 3. By random chance, our team had a rough match that time around.

However, we accept the fact that upon playing several games, and upon the alliance partners and opponents playing several games as well, the third option becomes less and less relevant. Thus we have now boiled down the reason for the wildly varying match diff down to two reasons that we know with relative certainty. This is incredibly powerful, and is the essence of the algorithm (but perhaps one could say, executed in reverse).

> Let's call the difference between the match diff of a match and a team's average match diff, the `deviation`.

In the above example we looked at a random match diff of a team compared to that team's average. But let's try something else: for a given match, calculate how much the match diff varied from the average for *everyone else in the match* but our team in question. It's easier with numbers: let's say the opponents were normally losing by 10 points (md = `-10`) and the alliance partner was normally losing by 30 (md = `-30`). If we take the previous example where our team loses by 20 points, then the deviation for the opponents is **`+30`** (`20 - (-10)`). That means our team was ineffective at preventing the opponent teams from getting points, since they were able to get more points than they got on average. But on the alliance partner side, the deviation is **`+10`** (`(-20) - (-30)`). This tells us that our team displayed a positive influence on the alliance partner's average point scoring ability. Averaging the deviations of our opponents across all of our matches is analogous to, but not equal to, the **Offensive Powerscore**. Likewise, averaging the deviations of our alliance partners across all of our matches is analogous to, but not equal to, the **Defensive Powerscore**. A mixture of these two is the actual **Powerscore**.

Powerscores always lie between 0 and 100, with most values lying around 50. A simple way to understand what Powerscore means is to see teams with scores above 50 as positive influences on their game outcomes, whereas teams with scores below 50 were negative influences on their game outcomes.

---
### The Design of VRC Tracker
Unlike an app that seeks broad adoption, VRC Tracker is designed for the target audience of competitors in the VEX Robotics Competition. In order to be adopted with other competitors like the official "VEX Via" and the widely popular "VRC Roboscout" designed by the world-renowned team 229V "Ace Robotics", VRC Tracker needed certain unique aspects that gave it a unique use case. These aspects include: <b>A proprietary algorithm, scouting utility, intuitive interface, and gamification.</b>

#### Proprietary Algorithm: Powerscore
VRC Tracker actually began as just the Powerscore algorithm, where a user (often myself) would input the match results as a spreadsheet and an algorithm would return a competition distribution of scores as a spreadsheet. From the get go, this algorithm was unique, and had great promise to be more useful in match analysis than its competitors. A lot of other calculations can stem from the base algorithm, like OPS/DPS, career graphs, accolades, and more.

#### Scouting Utility: Easily Visible Stats, Scannable Cards, Etc.
For participants of VEX Robotics, a high priority is to be able to scout other teams as well as flaunt their stats easily. For this, VRC Tracker works quickly on mobile, allowing for teams to efficiently get the stats of other teams, and to show their stats on demand. Link previews allow for the sending of team statistics to be seamless inside online chats, and scannable team cards are great for tracking teams' rankings within a competition.

#### Intuitive Interface: Connected Data
A core principle of an intutive interface, especially for people want to quickly find and share information, is to have all the different pages easily accessible from one another. This means for example having the competition pages accessible from Team dashboards, or having backlinks from the comp distributions to the individual career pages, having ranks accessible from the career page, or having the landing page always accessible from all other pages.

#### Gamification: Ranks, Graphs, XP, Accolades, Titles
The display of ranks, career graphs, experience points, team accolades, and team titles serve to gamify VEX Robotics, making it more competitive but also more playful, akin to a video game. Hopefully by making VRC Tracker more mainstream we can inspire future competitive robotics participants to take part in the engaging, interactive, community-aspect of the activity as well.
