var RESULT_PER_PAGE = 30

window.onload = function() {
    localStorage.setItem("searchType", 0)

    document.getElementById("search-btn").addEventListener("click", function() {
        clear()
        var element = document.getElementById("search-input");

        if(element.value.length === 0) {
            return;
        }
        
        localStorage.setItem("query", element.value)

        sendSearchQuery(0, RESULT_PER_PAGE, true)
    });

    document.getElementById("ordinary-search").addEventListener("click", function() {
        var selectedSearch = document.getElementById("selected-search-type")
        selectedSearch.innerHTML = "Избрано търсене: Обикновено търсене";
        localStorage.setItem("searchType", 0)
    });

    document.getElementById("advanced-search").addEventListener("click", function() {
        var selectedSearch = document.getElementById("selected-search-type")
        selectedSearch.innerHTML = "Избрано търсене: Разширено търсене";
        localStorage.setItem("searchType", 1)
    });

    document.getElementById("export-btn").addEventListener("click", function() {
        tableToExcel("main-table", "results")
    });

    $(document).keypress(function(e){
        if (e.which == 13){
            $("#search-btn").click();
        }
    });
};

function sendSearchQuery(from, size, initial=false) {
    var query = localStorage.getItem("query")
    var type = parseInt(localStorage.getItem("searchType"))

    console.log(type)

    if(type == 0) {
        sendOrdinarySearchQuery(query, from, size, initial)
    } else if(type == 1) {
        sendAdvancedSearchQuery(query, from, size, initial)
    }
}

function sendOrdinarySearchQuery(value, from, size, initial) {
    ajax("http://localhost:8081/open?path=/home/angel/Desktop/AI/IR/Data/1883-1884/05-06.pdf", {})
    if(initial) {
        ajax("http://localhost:8081/ordinary_search/count?phrase_new=" + value + "&phrase_old=" + 
            convert(value), {}, buildPages)
    }
    
    ajax("http://localhost:8081/ordinary_search?phrase_new=" + value + "&phrase_old=" + 
        convert(value) + "&from=" + from + "&size=" + size, {}, fillTable)
}

function sendAdvancedSearchQuery(value, from, size, initial) {
    if(initial) {
        ajax("http://localhost:8081/advanced_search/count?phrase_new=" + value + "&phrase_old=" + 
            convert(value), {}, buildPages)
    }
    
    ajax("http://localhost:8081/advanced_search?phrase_new=" + value + "&phrase_old=" + 
        convert(value) + "&from=" + from + "&size=" + size, {}, fillTable)
}

function clear() {
    clearTable()
    clearPages()
    var type = localStorage.getItem("searchType")
    localStorage.clear()
    localStorage.setItem("searchType", type)
}

function clearTable() {
    var table = document.querySelector("#files-container");

    if (!table.classList.contains("non-visible")) {
        table.classList.add("non-visible");
    }

    document.querySelector("#main-table tbody").innerHTML = "";
}

function clearPages() {
    document.querySelector("#pages").innerHTML = "";
}

function clearTableRows() {
    document.querySelector("#main-table tbody").innerHTML = "";
}

function openFile(filePath) {
    window.open("http://localhost:8081/open?path=" + filePath, "_blank");
}