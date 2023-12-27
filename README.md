# PowerScore
## The Most Powerful Team Evaluation Algorithm for VEX Robotics*
###### *may be mildly opinionated

---
The PowerScore algorithm is an advanced team evaluation algorithm that takes into account a team's ability to bring its own alliance to victory, as well as analyze how efficiently a team shuts its opponents down. The algorithm is multilayered and makes use of many different mathematical functions to work. The end result is a scale of localized values that represent the varying levels of match "power" shown by teams at a VEX Robotics Competition.

### How to Use (Unpackaged)
#### Download Program
Download this Git repository as a zip file onto your computer and unpack it. Whenever you want to run the program, click `main.py` within the folder named `src`. When I eventually migrate this application from a standalone python program to either a packaged executable or a webpage, this step will be far less complicated.

#### Download XLS Results
On the RobotEvents page for any competition, navigate to the "results" tab, then click the division that you want to analyze. Click "Results XLS". It will save a spreadsheet into your computer. Save this spreadsheet somewhere where it can be accessed easily.

#### Run the Program
Run the program `main.py`, and once the window opens up, click "Import XLS". You will be prompted to select an XLS file on your computer. Select the one you have downloaded. In a very short moment, a notepad window will pop up that contains the PowerScore distribution of that competition. It is formatted so that the results can be readily pasted into Microsoft Excel or Google Sheets.

### Roadmap
#### b1.0.1: ALGORITHM (complete) <<<
- A base version of the algorithm that can take a spreadsheet of match results and generate a .txt document of results that can be pasted into a sheet of its own for analysis.

#### b1.0.2: GUI (complete)
- A bare bones UI to give users the abilty to input a match they want to analyze and a way to display the algorithm's output.

#### b1.0.3: AUTOMATION
- A simple tool to either scrape RobotEvents or use the RobotEvents API to grab match results directly as opposed to having to download them manually.