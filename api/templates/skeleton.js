const overlayButton = document.getElementById('overlayButton');
const imageOverlay = document.querySelector('.imageOverlay');

overlayButton.addEventListener("click", function() {
    imageOverlay.style.backgroundImage = 'url("https://www.dropbox.com/scl/fi/gv0549s6zm6vij93ggf9p/Skeleton.gif?rlkey=dyv46jhjc5bkqseumcsvcw2eo&st=5ikvb3uo&raw=1")';
    imageOverlay.style.display = 'block';
});