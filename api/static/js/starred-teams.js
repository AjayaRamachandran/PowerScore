// Function to open the right side panel of starred teams when the panel button is clicked
function openPanel() {
    const debug = document.getElementById('debug').value;
    const page = document.getElementById('page').value;
    var panel = document.getElementById('panel').value;
    panelItem = document.getElementById('panel')
    console.log(`Debug = ${debug}`)
    const teamList = document.getElementById('team-list');
    const starredTeams = JSON.parse(localStorage.getItem('starredTeams')) || [];

    teamList.style.display = "flex"
    
    console.log(panel)
    if (panel === "Y") {
        panel = "N"
    } else {
        panel = "Y"
    }
    panelItem.setAttribute("value", panel)
    console.log(panel)
    const expand = document.getElementById('expand');
    const retract = document.getElementById('retract');

    if (panel === "Y") {
        expand.style.display = 'none';
        retract.style.display = 'flex';
    } else {
        retract.style.display = 'none';
        expand.style.display = 'flex';
    }

    teamList.innerHTML = '';
    if (panel === "Y") {
        if (starredTeams.length === 0) {
            const title = document.createElement('div');
            title.className = "starred-team none";
            title.textContent = "You have no starred teams.";
            title.style.fontWeight = "500";
            title.style.color = "#5bacbd";
            teamList.appendChild(title);
        } else {
            if (page === "splash" && starredTeams.length > 0) {
                const title = document.createElement('div');
                title.className = "starred-team";
                title.textContent = "Starred Teams:";
                title.style.fontWeight = "900";
                title.style.color = "#5bacbd";
                teamList.appendChild(title);
            }

            starredTeams.forEach(team => {
                const teamItem = document.createElement('div');
                teamItem.className = "starred-team";
                
                const teamLink = document.createElement('a');
                //teamLink.className = "starred-team";
                teamLink.textContent = team;
                if (debug === "Y") {
                    teamLink.href = `http://localhost:5000/teams?query=${team}`;
                } else {
                    teamLink.href = `https://powerscore.vercel.app/teams?query=${team}`;
                }
                //teamLink.target = "_blank"; // Optional: open in a new tab
                teamLink.style.textDecoration = 'none';
                //teamLink.style.color = 'inherit';
                const teamIcon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
                teamIcon.setAttribute("width", "28");
                teamIcon.setAttribute("height", "28");
                teamIcon.setAttribute("viewBox", "0 0 24 24");
                teamIcon.setAttribute("fill", "#ffffff");
                teamIcon.classList.add("feather", "feather-star");

                const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
                path.setAttribute("d", "M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z");

                teamIcon.appendChild(path);

                teamItem.appendChild(teamIcon);
                teamItem.appendChild(teamLink);
                teamList.appendChild(teamItem);
            });
        }
    } else {
        teamList.style.display = "none"
    }
}

// Function to load starred teams from localStorage
function loadStarredTeams() {
    const debug = document.getElementById('debug').value;
    const page = document.getElementById('page').value;
    console.log(`Debug = ${debug}`)
    const teamList = document.getElementById('team-list');
    const starredTeams = JSON.parse(localStorage.getItem('starredTeams')) || [];

    teamList.innerHTML = '';
    if (page === "splash" && starredTeams.length > 0) {
        const title = document.createElement('div');
        title.className = "starred-team";
        title.textContent = "Starred Teams:";
        title.style.fontWeight = "900";
        title.style.color = "#5bacbd";
        teamList.appendChild(title);
    }

    if (page === "splash" || page === "index") {
        starredTeams.forEach(team => {
            const teamItem = document.createElement('div');
            teamItem.className = "starred-team";
            
            const teamLink = document.createElement('a');
            //teamLink.className = "starred-team";
            teamLink.textContent = team;
            if (debug === "Y") {
                teamLink.href = `http://localhost:5000/teams?query=${team}`;
            } else {
                teamLink.href = `https://powerscore.vercel.app/teams?query=${team}`;
            }
            //teamLink.target = "_blank"; // Optional: open in a new tab
            teamLink.style.textDecoration = 'none';
            //teamLink.style.color = 'inherit';
            const teamIcon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
            teamIcon.setAttribute("width", "28");
            teamIcon.setAttribute("height", "28");
            teamIcon.setAttribute("viewBox", "0 0 24 24");
            teamIcon.setAttribute("fill", "#ffffff");
            teamIcon.classList.add("feather", "feather-star");
    
            const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
            path.setAttribute("d", "M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z");
    
            teamIcon.appendChild(path);
    
            teamItem.appendChild(teamIcon);
            teamItem.appendChild(teamLink);
            teamList.appendChild(teamItem);
        });
    }
    loadStar();
}

// Function to display the correct star version on page load
function loadStar() {
    let starText = document.getElementById('star-text');
    const emptyStar = document.getElementById('empty-star');
    const filledStar = document.getElementById('filled-star');
    let starredTeams = JSON.parse(localStorage.getItem('starredTeams')) || [];

    const teamCode = document.getElementById('team-code').value;
    if (starredTeams.includes(teamCode)) {
        starText.textContent = 'Unstar';
        starText.style.fontWeight = '400';
        starText.style.color = '#666666';
    } else {
        starText.textContent = 'Star'
        starText.style.fontWeight = '400';
        starText.style.color = '#000000';
    }

    
    if (starredTeams.includes(teamCode)) {
        emptyStar.style.display = 'none';
        filledStar.style.display = 'block';
    } else {
        emptyStar.style.display = 'block';
        filledStar.style.display = 'none';
    }
}

// Function to star a team
function starTeam() {
    const teamCode = document.getElementById('team-code').value;
    let starredTeams = JSON.parse(localStorage.getItem('starredTeams')) || [];

    console.log(starredTeams);
    if (!starredTeams.includes(teamCode)) {
        starredTeams.push(teamCode);
    } else {
        starredTeams = starredTeams.filter(item => item !== teamCode);
    }
    localStorage.setItem('starredTeams', JSON.stringify(starredTeams));
    loadStarredTeams();
}

window.onload = loadStarredTeams;