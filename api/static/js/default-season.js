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

    // Set the default selected option in the dropdown
    if (defaultOption) {
        dropdown.value = defaultOption;
    }
    else {
        dropdown.value = "190";
    }
});