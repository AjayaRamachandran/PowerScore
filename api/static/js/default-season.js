document.addEventListener('DOMContentLoaded', function () {
    // Function to get URL parameters
    function getUrlParameter(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        var regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        var results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // Get the dropdown element
    var dropdown = document.getElementById('seasons');

    // Get the default option value from the URL parameter
    var defaultOption = getUrlParameter('season');

    var values = ["V5RC 24-25: High Stakes", "VRC 23-24: Over Under", "VRC 22-23: Spin Up", "VRC 21-22: Tipping Point"];
    var data = ["190", "181", "173", "154"];
    // Set the default selected option in the dropdown
    if (defaultOption) {
        dropdown.value = defaultOption;
    }
    else {
        dropdown.value = data[values.indexOf(localStorage.getItem("preference1"))];
    }
});