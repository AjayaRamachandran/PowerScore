const selectElement = document.getElementById('seasons');
const formElement = document.getElementById('myForm');

selectElement.addEventListener('change', () => {
    formElement.submit();
});

function reloadCSS() {
    var links = document.getElementsByTagName("link");
    for (var i = 0; i < links.length; i++) {
        var link = links[i];
        if (link.rel === "stylesheet" && link.id != "freeze") {
            link.href = link.href.split("?")[0] + "?reload=" + new Date().getTime();
        }
    }
}
reloadCSS();