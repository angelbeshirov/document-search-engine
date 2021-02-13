window.onload = function() {
    retrieveAndPopulate();
};

window.onclick = function(event) {
    var dropdowns = document.querySelectorAll("#main-table tbody .file-menu")
    for (var i = 0; i < dropdowns.length; i++) {
        var openDropdown = dropdowns[i].querySelector(".dropdown-menu");
        if (!openDropdown.classList.contains('non-visible')) {
            openDropdown.classList.add('non-visible');
        }
    }
    if (event.target.matches('.column5') || event.target.matches('.file-menu')) {
        event.target.querySelector(".dropdown-menu").classList.remove("non-visible");
    }
}

function retrieveAndPopulate() {
    ajax("http://localhost:8081/images/getAll", {}, populate);
}

function clearTable() {
    document.querySelector("#main-table tbody").innerHTML = "";
}

function populate(xhr) {
    if (xhr.status == 200 && xhr.response) {
        var tableBody = document.querySelector("#main-table tbody");
        console.log(xhr.response);
        var files = JSON.parse(xhr.response);
        for (var i = 0; i < files.length; i++) {
            var file = files[i];
            var tr = document.createElement("tr");
            populateRow(tr, file);
            tableBody.appendChild(tr);
        }
    }
}

function populateRow(tr, file) {
    tr.appendChild(createTD(file.name, ["column1"]));
    tr.appendChild(createTD(file.size + " B", ["column2"]));
    tr.appendChild(createTD(file.uploadedOn, ["column3"]));
    tr.appendChild(createTD(file.extension, ["column4"]));
    tr.appendChild(addActionsToFile());
}

function createTD(value, classes) {
    var col = document.createElement("td");
    col.innerHTML = value;
    for (var i = 0; i < classes.length; i++) {
        col.classList.add(classes[i]);
    }

    return col;
}

function deleteFile(fileName) {
    var settings = {};
    settings["method"] = "DELETE";
    // will this work with cyrilic filename? encodeURI?
    ajax("http://localhost:8081/images/delete?file=" + fileName, settings, handleResponseFromDelete);
}

function handleResponseFromDelete(xhr) {
    if (xhr.status == 200) {
        clearTable();
        retrieveAndPopulate();
    } else {
        alert("There was an error while deleting this file!");
    }
}
