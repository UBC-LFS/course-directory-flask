// Sessions
function selectSession(year, termCode, termName) {
    sessionInput = document.getElementById("sessionInput");
    sessionInput.value = String(year) + " " + termName;
}
// Generate the session options
function generateSessions(year, termCode, termName) {
    sessionDropDown = document.getElementById("sessionDropDown");
    const sessionLi = document.createElement("li");
    sessionLi.innerHTML = String(year) + " " + termName
    sessionLi.classList.add("dropdownLi");
    sessionLi.addEventListener("click", function() {
        hideDropdown('sessionDropDown') // Hides the dropdown menu
        selectSession(year, termCode, termName) // make this select that session and update courses to display
        // Make this get the current selected department
        const deptName = document.getElementById("deptInput").value
        const searchBarInput = document.getElementById("searchBar").value
        displayCourses(year, termCode, deptName, searchBarInput)
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

// For displaying dropdown menu options
function showDropdown(idName) {
    dropdown = document.getElementById(idName);
    dropdown.style.display = "block";
}

function hideDropdown(idName) {
    dropdown = document.getElementById(idName);
    dropdown.style.display = "none";
}


// Select default session
// Make the term change depending on the date
selectSession(currentYear, "S", "Summer")

// Sessions ^^^

// Dept
dropdownDeptOptions = ['- ALL -','APBI', 'FNH', 'FOOD', 'FRE', 'GRS', 'HUNU', 'LFS', 'LWS', 'PLNT', 'SOIL']

function selectDept(dept) {
    deptInput = document.getElementById("deptInput");
    deptInput.value = dept;
}

selectDept("- ALL -")

function generateDepts() {
    for (const dept in dropdownDeptOptions) {
        const deptName = dropdownDeptOptions[dept]
        deptDropDown = document.getElementById("deptDropDown");
        const deptLi = document.createElement("li");
        deptLi.innerHTML = deptName
        deptLi.classList.add("dropdownLi");
        deptLi.addEventListener("click", function() {
            hideDropdown('deptDropDown') // Hides the dropdown menu
            selectDept(deptName) // make this select that session and update courses to display
            // Gets the current selected year + term code from the input
            const year = document.getElementById("sessionInput").value.split(" ")[0]
            const termCode = document.getElementById("sessionInput").value.split(" ")[1][0]
            const searchBarInput = document.getElementById("searchBar").value
            displayCourses(year, termCode, deptName, searchBarInput)
        })
        deptDropDown.append(deptLi);
    }

}

generateDepts()
// Dept ^^^
