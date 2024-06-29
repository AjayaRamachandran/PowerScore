# PowerScore
## A Powerful Team Evaluation Algorithm for VEX Robotics

---
The PowerScore algorithm is an advanced team evaluation algorithm that takes into account a team's ability to bring its own alliance to victory, as well as analyze how efficiently a team shuts its opponents down. The algorithm is multilayered and makes use of many different mathematical functions to work. The end result is a scale of localized values that represent the varying levels of match "power" shown by teams at a VEX Robotics Competition.

### Elements of the Algorithm
Powerscore makes frequent use of the value named `matchDiff`. Put simply, it is the difference in score between a team and their opponent for a single match. Match diffs often vary, but we can establish an axiom to work off of. Namely, that as a team plays many matches, outside factors become less relevant toward establishing a relationship between the true skill differential of teams in a match and their respective match diffs. If we accept this axiom to be true, given the fact that it bears many similarities to the Central Limit Theorem, a lot of data can be extrapolated from it.

A team may average a match diff of `+30` across all their games. In other words, on average they win by 30 points. If in one randomly selected match they lose by, say, 20 points (having a match diff of `-20`), we can reasonably assume one of three things has occured.

###### 1. The team's alliance partner was significantly worse than the average alliance partner for our team.
###### 2. The team's opponent was significantly better than the average opponent for our team.
###### 3. By random chance, our team had a rough match that time around.

However, we accept the fact that upon playing several games, and upon the alliance partners and opponents playing several games as well, the third option becomes less and less relevant. Thus we have now boiled down the reason for the wildly varying match diff down to two reasons that we know with relative certainty. This is incredibly powerful, and is the essence of the algorithm (but perhaps one could say, executed in reverse).

**Let's call the difference between the match diff of a match and a team's average match diff, the `deviation`.**

In the above example we looked at a random match diff of a team compared to that team's average. But let's try something else: for a given match, calculate how much the match diff varied from the average for *everyone else in the match* but our team in question. It's easier with numbers: let's say the opponents were normally losing by 10 points (md = `-10`) and the alliance partner was normally losing by 30 (md = `-30`). If we take the previous example where our team loses by 20 points, then the deviation for the opponents is **`+30`** (`20 - (-10)`). That means our team was ineffective at preventing the opponent teams from getting points, since they were able to get more points than they got on average. But on the alliance partner side, the deviation is **`+10`** (`(-20) - (-30)`). This tells us that our team displayed a positive influence on the alliance partner's average point scoring ability. Averaging the deviations of our opponents across all of our matches is analogous to, but not equal to, the **Offensive Powerscore**. Likewise, averaging the deviations of our alliance partners across all of our matches is analogous to, but not equal to, the **Defensive Powerscore**. A mixture of these two is the actual **Powerscore**.

Powerscores always lie between 0 and 100, with most values lying around 50. A simple way to understand what Powerscore means is to see teams with scores above 50 as positive influences on their game outcomes, whereas teams with scores below 50 were negative influences on their game outcomes.

### Roadmap
#### b1.0.1: ALGORITHM (complete) 
- A base version of the algorithm that can take a spreadsheet of match results and generate a .txt document of results that can be pasted into a sheet of its own for analysis.

#### b1.0.2: AUTOMATION (complete)
- Use the RobotEvents API to grab match results for analysis.

#### b1.0.3: GUI (complete) <<<
- A web app to easily input teams and competitions, using the RobotEvents API and a python backend to work with the `flask` module and push a rich, interactive UI to users.
