# PowerScore
## The Most Powerful Team Evaluation Algorithm for VEX Robotics

---
The PowerScore algorithm is an advanced team evaluation algorithm that takes into account a team's ability to bring its own alliance to victory, as well as analyze how efficiently a team shuts its opponents down. The algorithm is multilayered and makes use of many different mathematical functions to work. The end result is a scale of localized values that represent the varying levels of match "power" shown by teams at a VEX Robotics Competition.

### Roadmap
#### b1.0.1: ALGORITHM (complete)
- A base version of the algorithm that can take a spreadsheet of match results and generate a .txt document of results that can be pasted into a sheet of its own for analysis.

#### b1.0.1: AUTOMATION (modified)
- A simple tool to either scrape RobotEvents or use the RobotEvents API to grab match results directly as opposed to having to download them manually.
##### This step was modified to no longer involve RobotEvents, but rather simply run off of imported spreadsheets.

#### b1.0.1: GUI (not yet started) <<<
- A bare bones UI to give users the abilty to input a match they want to analyze and a way to display the algorithm's output.