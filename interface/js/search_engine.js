var selected_search_type = 0

window.onload = function() {
    document.getElementById("search-btn").addEventListener("click", function() {
        clearTable()
        var element = document.getElementById("search-input");

        if(element.value.length === 0) {
            return;
        }

        if (selected_search_type == 0) {
            send_ordinary_search_query(element.value)
        } else if (selected_search_type == 1) {
            send_advanced_search_query(element.value)
        }
    });

    document.getElementById("ordinary-search").addEventListener("click", function() {
        var selected_search = document.getElementById("selected-search-type")
        selected_search.innerHTML = "Избрано търсене: Обикновено търсене";
        selected_search_type = 0
    });

    document.getElementById("advanced-search").addEventListener("click", function() {
        var selected_search = document.getElementById("selected-search-type")
        selected_search.innerHTML = "Избрано търсене: Разширено търсене";
        selected_search_type = 1
    });

    document.getElementById("export-excel-btn").addEventListener("click", function() {
        tableToExcel("main-table", "results")
    });
    
    document.getElementById("export-pdf-btn").addEventListener("click", function() {
        tableToExcel("main-table", "results")
    });
};

function clearTable() {
    var table = document.querySelector("#main-table");

    if (!table.classList.contains('non-visible')) {
        table.classList.add('non-visible');
    }
    document.querySelector("#main-table tbody").innerHTML = "";
}