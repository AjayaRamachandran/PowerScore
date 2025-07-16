// js for the preferences

function getDefaultSeason(prefName) {

    const parentDiv = document.getElementById(prefName);
    var preference = ""

    if (prefName === "preference1") {
        preference = localStorage.getItem(prefName) || "VRC 23-24: Over Under";
        var values = ["V5RC 25-26: Push Back", "V5RC 24-25: High Stakes", "VRC 23-24: Over Under", "VRC 22-23: Spin Up", "VRC 21-22: Tipping Point"];
        var data = ["197", "190", "181", "173", "154"];
    } else if (prefName === "preference2") {
        preference = localStorage.getItem(prefName) || "Natural";
        values = ["Dark", "Natural"];
        data = ["0", "1"];
    }
    var select = document.createElement("select");
    select.className = "dropdown";
    select.name = "seasons";
    select.id = "seasons";
    select.setAttribute("visual", "bg")
    for (let i = 0; i < data.length; i++) {
        // creates an element that is part of the dropdown
        var option = document.createElement("option");
        option.value = data[i];
        option.text = values[i];
        // after giving the dropdown item info, it appends the item to the dropdown
        select.appendChild(option);
    }
    select.value = data[values.indexOf(preference)];

    select.addEventListener('change', () => {
        const newPreference = values[data.indexOf(select.value)];
        localStorage.setItem(prefName, newPreference);
    });
    
    parentDiv.appendChild(select);//.appendChild(select);

    return preference;
}
// color: #98c8d1;
function handleAppearance() {
    preference = localStorage.getItem("preference2") || "Natural";
    document.addEventListener('DOMContentLoaded', function() {
        const bgElements = document.querySelectorAll('[visual="bg"]');
        for (const bgElement of bgElements) {
            if (preference === "Dark") {
                bgElement.style.backgroundColor = '#171717';
                console.log("1")
            }
        }
        const subtitles = document.querySelectorAll('[visual="sub"]');
        for (const sub of subtitles) {
            if (preference === "Dark") {
                sub.style.color = '#aaaaaa';
                console.log("2")
            } else {
                sub.style.color = '#b6cdd1';
                console.log("2")
            }
        }
        const tints = document.querySelectorAll('[visual="tint"]');
        for (const tint of tints) {
            if (preference === "Dark") {
                tint.style.backgroundColor = '#333333';
                console.log("3")
            }
        }
        const shades = document.querySelectorAll('[visual="shade"]');
        for (const shade of shades) {
            if (preference === "Dark") {
                shade.style.backgroundColor = '#000000';
                console.log("4")
            }
        }
    });
}

function sendSpecifiedSeason() {
    document.addEventListener('DOMContentLoaded', function() {
        var values = ["V5RC 25-26: Push Back", "V5RC 24-25: High Stakes", "VRC 23-24: Over Under", "VRC 22-23: Spin Up", "VRC 21-22: Tipping Point"];
        var data = ["197", "190", "181", "173", "154"];
        
        var element = document.getElementById("season");
        element.setAttribute("value", (data[values.indexOf(localStorage.getItem("preference1"))] || "190"));
        //console.log(data[values.indexOf(localStorage.getItem("preference1"))] || "190");
    });
}

// sendSpecifiedSeason ensures that the season parameter in the URL is set to the correct one
sendSpecifiedSeason();
handleAppearance();