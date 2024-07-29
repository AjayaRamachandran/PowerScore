document.getElementById('kudos-button').addEventListener('click', function() {
    const userID = this.getAttribute('team');
    let kudos = parseInt(this.getAttribute('kudos'));

    console.log(userID)
    fetch('/give-kudos', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ team : userID }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Increment the kudos count
            kudos += 1;
            this.setAttribute('kudos', kudos);

            // Find the <b> element within the button and update its text content
            const kudosCountElement = this.querySelector('b');
            if (kudosCountElement) {
                kudosCountElement.textContent = kudos;
            }
        } else {
            console.error("Failed to give kudos");
        }
    })
    .catch(error => {
        console.error("Error:", error);
    });
});