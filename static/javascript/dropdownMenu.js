function selectSession(year, termCode, termName) {
    sessionInput = document.getElementById("sessionInput");
    sessionInput.value = String(year) + " " + termName;
}
// Generate the session options
function generateSessions(year, termCode, termName) {
    sessionDropDown = document.getElementById("sessionDropDown");
    const sessionLi = document.createElement("li");
    sessionLi.innerHTML = String(year) + " " + termName
    // sessionLi.className
    sessionLi.addEventListener("click", function() {
        selectSession(year, termCode, termName) // make this select that session and update courses to display
    })
    sessionDropDown.append(sessionLi);
}

var currentYear = new Date().getFullYear();
generateSessions(currentYear + 1, "W", "Winter"); // next year
generateSessions(currentYear + 1, "S", "Summer"); // next year
generateSessions(currentYear, "W", "Winter"); // current year
generateSessions(currentYear, "S", "Summer"); // current year
generateSessions(currentYear - 1, "W", "Winter"); // previous year
generateSessions(currentYear - 1, "S", "Summer"); // previous year

function displaySessions() {
    
}

LFSDepts = ['APBI', 'FNH', 'FOOD', 'FRE', 'GRS', 'HUNU', 'LFS', 'LWS', 'PLNT', 'SOIL']
