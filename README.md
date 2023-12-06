# Skill-Issue
## The VRC Skills Copilot

---
Skill Issue is a powerful desktop-based application that allows individuals to analyze their VRC Robot Skills with time. The application allows users to input unofficial skills scores, see others skills scores online, observe and analyze their own skills progression, and export data for use in their engineering notebooks. The program also features a powerful algorithm which can tokenize and break down skills circuits, and give tips on how to improve it.

### Roadmap
#### b1.0.1: GUI (in progress) <<<
- Create a custom GUI module in Python based on the Pygame library to easily display all possible GUI elements, from buttons, text boxes, sliders, scrollable lists, etc.

#### b1.0.2: Working Model (planned)
- Finalize a first working model of the program that allows inputting of skills scores, creation of graphs and exporting data, as well as the ability to access the dummy scroll menu of online skills scores.

#### b1.0.3: Web Syncing (planned)
- Create a framework for the program to directly access an online data storage system that contains all posted unofficial skills scores to display on the "feed". Finalize authentication system for teams to ensure no one else but them can post skills scores for their team.

#### b1.0.4: Deployment (planned)
- Host a website where users can download the program onto their computers and try it for themselves.

#### b1.0.5: Tokenization Algorithm (planned)
- Develop algorithm to break down skills scores, use a combination of prewritten knowledge and online resources to compile tips for the user.

---

### A Brief Breakdown of how the Tokenization Algorithm May Work (AutoGrant)
In order to effectively analyze how a skills score is achieved, we can ask players upon entering their skills score online a few questions regarding what the primary goal of their skills run was, which elements they had in their skills run, and so on. By doing this, we begin to associate certain attributes of skills runs with certain ranges of scores. We can break this distribution into `x` different segments. When trying to analyze ways to improve an individual's skills score, we first find which segment of the distribution their score is in. We find common attributes of skills runs within this segment and use the difference between these attributes and the attributes of skills runs one segment above to generate a response. Each difference in attributes is mapped to a sentence "token", with removal of a feature or practice receiving a token of value `1`, changing a feature a value of `2`, and adding a feature value `3`. Assembling these sentence tokens may produce a response akin to the one below:

`Your unofficial Programming Skills Average was 115, which places you in the 75th percentile of World Skills scores. Many players with similar skills scores have a match load routine to launch the 44 triballs across the field, and a method of pushing triballs under the goal. In order to improve your skills score, you could try the following: Transitioning from launching triballs at a slow rate to launching triballs at a faster rate, removing potential wait times in the code, and adding multiple angles to pushing triballs under the goal.`
