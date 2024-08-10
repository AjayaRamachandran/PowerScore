<p align="center">
<img src="https://www.dropbox.com/scl/fi/jk33040qbewi0lqfs1tbe/PS2.png?rlkey=75wqlp7ptpr9n6koeoi6ew73w&st=dequz2hg&raw=1" width="150" height ="150">
<h1 align="center">PowerScore on VRC-Tracker</h1>
</p>

<p align="center">
<img src="https://img.shields.io/badge/Python-navy?logo=python"> <img src="https://img.shields.io/badge/JavaScript-yellow?logo=javascript"> <img src="https://img.shields.io/badge/HTML-orange?logo=html5">  *  <img src="https://img.shields.io/badge/Vercel-black?logo=Vercel"> <img src="https://img.shields.io/badge/Flask-gray?logo=flask">
</p>

## VRC-Tracker: A Flask Web Application on Vercel

<b>[VRC-Tracker](https://powerscore.vercel.app/)</b> is a serverless deployment on Vercel, built with the P-J-H stack (Python, JavaScript, HTML). Python is interfaced with the frontend using the [Flask WSGI](https://flask.palletsprojects.com/en/3.0.x/), which internally uses [Werkzeug](https://werkzeug.palletsprojects.com/en/3.0.x/) and [Jinja](https://jinja.palletsprojects.com/en/3.1.x/). The application is designed to work without the need for server-side file storage, so that it may be deployed on any service. To download and run it locally, download this repository, change "Debug" to "Y" in `config.txt` and run `app.py` on your local machine; the application will be available on your localhost.

### Server-side requirements (for running locally)
VRC-Tracker makes frequent requests to the <b>[RobotEvents API](https://www.robotevents.com/api/v2)</b>. This means you will need a stable internet connection. If you are planning on running the program locally, go to the RobotEvents API site and get a set of API keys to use. Create a file called "osEmul.py" setup as shown below:
```python
class environ():
    def get(key):
        apiKeys = {
            "API_KEY1" : "Enter Key Here!"
            # add more api keys here
            }
        return apiKeys[key]
```
---
### What is the PowerScore Algorithm?
In VEX Robotics, teams play to compete for high points while trying to keep their opponents from doing the same thing. Games are set up by "alliances", which are randomly assigned pairs of teams that oppose a different pair of teams. Since individual statistics of a team in a match are not tracked in VEX Robotics, it can be difficult to determine how one team contributes to the outcome of their game. This knowledge is important for picking the correct partner in the elimination phase of the tournament. Thus, algorithms like OPR/DPR/CCWM, AdamScore, TrueSkill, and others have tried to calculate this "individual contribution", but each one has its own drawbacks. Powerscore has been rated the most accurate to a team's actual skill by numerous VEX robotics participants. Here's how it works.

The PowerScore algorithm is an advanced team evaluation algorithm that takes into account a team's ability to bring its own alliance to victory, as well as analyze how efficiently a team shuts its opponents down. The algorithm is multilayered and makes use of many different mathematical functions to work. The end result is a scale of localized values that represent the varying levels of match "power" shown by teams at a VEX Robotics Competition.

#### Elements of the Algorithm
Powerscore makes frequent use of the value named `matchDiff`. Put simply, it is the difference in score between a team and their opponent for a single match. Match diffs often vary, but we can establish an axiom to work off of. Namely, that as a team plays many matches, outside factors become less relevant toward establishing a relationship between the true skill differential of teams in a match and their respective match diffs. If we accept this axiom to be true, given the fact that it bears many similarities to the Central Limit Theorem, a lot of data can be extrapolated from it.

A team may average a match diff of `+30` across all their games. In other words, on average they win by 30 points. If in one randomly selected match they lose by, say, 20 points (having a match diff of `-20`), we can reasonably assume one of three things has occured.

##### 1. The team's alliance partner was significantly worse than the average alliance partner for our team.
##### 2. The team's opponent was significantly better than the average opponent for our team.
##### 3. By random chance, our team had a rough match that time around.

However, we accept the fact that upon playing several games, and upon the alliance partners and opponents playing several games as well, the third option becomes less and less relevant. Thus we have now boiled down the reason for the wildly varying match diff down to two reasons that we know with relative certainty. This is incredibly powerful, and is the essence of the algorithm (but perhaps one could say, executed in reverse).

##### Let's call the difference between the match diff of a match and a team's average match diff, the `deviation`.

In the above example we looked at a random match diff of a team compared to that team's average. But let's try something else: for a given match, calculate how much the match diff varied from the average for *everyone else in the match* but our team in question. It's easier with numbers: let's say the opponents were normally losing by 10 points (md = `-10`) and the alliance partner was normally losing by 30 (md = `-30`). If we take the previous example where our team loses by 20 points, then the deviation for the opponents is **`+30`** (`20 - (-10)`). That means our team was ineffective at preventing the opponent teams from getting points, since they were able to get more points than they got on average. But on the alliance partner side, the deviation is **`+10`** (`(-20) - (-30)`). This tells us that our team displayed a positive influence on the alliance partner's average point scoring ability. Averaging the deviations of our opponents across all of our matches is analogous to, but not equal to, the **Offensive Powerscore**. Likewise, averaging the deviations of our alliance partners across all of our matches is analogous to, but not equal to, the **Defensive Powerscore**. A mixture of these two is the actual **Powerscore**.

Powerscores always lie between 0 and 100, with most values lying around 50. A simple way to understand what Powerscore means is to see teams with scores above 50 as positive influences on their game outcomes, whereas teams with scores below 50 were negative influences on their game outcomes.

---
### PowerScore API
A PowerScore API may exist soon. If you're interested, leave a star!
