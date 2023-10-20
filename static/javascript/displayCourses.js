var coursesPerPage = 40; // Number of courses to be displayed per page

function getSelectedPagination() {
    const options = document.getElementById("paginationUl").children;
    for (let i = 0; i < options.length; i++) {
        if (options[i].classList.contains("selected-pagination-option")) {
            return parseInt(options[i].innerHTML);
        }
    }
    // Default case
    return parseInt(1);
}
function selectPagination(pageOption) {
    const coursesTable = document.getElementById("coursesContainer");
    const lastPageNumber = document.getElementById("paginationUl").children.length - 2;
    if (pageOption == "&lt;") { // <
        // Get current selected option and subtract 1 or go to last if at 1
        const selectedPagination = getSelectedPagination()
        if (selectedPagination == 1) {
            selectPagination(lastPageNumber);
        }
        else {
            selectPagination(getSelectedPagination() - 1);
        }
    }
    else if (pageOption == "&gt;") { // >
        // Get current selected option and add 1 or go to 1 if at the end
        const selectedPagination = getSelectedPagination()
        if (selectedPagination == lastPageNumber) {
            selectPagination(1);
        }
        else {
            selectPagination(getSelectedPagination() + 1);
        }
    }
    else {
        // Added selected class to button
        const options = document.getElementById("paginationUl").children;
        for (let i = 0; i < options.length; i++) {
            if (pageOption == options[i].innerHTML) {
                options[i].classList.add("selected-pagination-option")
            }
            else {
                options[i].classList.remove("selected-pagination-option")
            }
        }
        // Figures out which courses to display
        const start = (pageOption - 1) * coursesPerPage;
        const end = (pageOption * coursesPerPage) - 1;
        for (let i = 0; i < coursesTable.children.length; i++) {
            // Course belongs in page? Make it visible
            if (start <= i && i <= end) {
                coursesTable.children[i].style.display = "table-row";
            }
            // Course does not belong in page? Hide it
            else {
                coursesTable.children[i].style.display = "none";
            }
        }
    }
}

function addPaginationOption(value) {
    const paginationUl = document.getElementById("paginationUl");
    const paginationLi = document.createElement("li");
    paginationLi.innerHTML = value;
    paginationLi.classList.add("paginationLi");
    paginationLi.addEventListener("click", function() {
        // Filter courses
        selectPagination(this.innerHTML);
    })
    paginationUl.appendChild(paginationLi);
}

function makePagination(numberOfCourses) {
    const numberOfPages = Math.ceil(numberOfCourses/coursesPerPage);
    // Clears pagination options
    document.getElementById("paginationUl").innerHTML = "";
    addPaginationOption("&lt;")
    for (let i = 1; i <= numberOfPages; i++) {
        addPaginationOption(i)
    }
    addPaginationOption("&gt;")
}

