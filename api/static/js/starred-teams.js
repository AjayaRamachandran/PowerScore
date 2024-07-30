// Function to load starred teams from localStorage
function loadStarredTeams() {
    const teamList = document.getElementById('team-list');
    const starredTeams = JSON.parse(localStorage.getItem('starredTeams')) || [];

    teamList.innerHTML = '';
    starredTeams.forEach(team => {
        const teamItem = document.createElement('div');
        teamItem.textContent = team;
        teamList.appendChild(teamItem);
    });
}

// Function to star a team
function starTeam() {
    const teamCode = document.getElementById('team-code').value;
    if (teamCode) {
        let starredTeams = JSON.parse(localStorage.getItem('starredTeams')) || [];
        if (!starredTeams.includes(teamCode)) {
            starredTeams.push(teamCode);
            localStorage.setItem('starredTeams', JSON.stringify(starredTeams));
            loadStarredTeams();
        } else {
            alert('Team already starred.');
        }
        document.getElementById('team-code').value = '';
    } else {
        alert('Please enter a team code.');
    }
}