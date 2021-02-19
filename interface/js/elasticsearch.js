function ajax(url, settings, callback) {
    if (settings) {
        var xhr = new XMLHttpRequest();
        xhr.withCredentials = true;
        xhr.onload = function() {
            if (callback) {
                callback(xhr);
            }
        };
        xhr.open(settings.method || "GET", url, true);
        if (settings.method == "POST") {
            xhr.setRequestHeader("Content-Type", "application/json");
        }
        xhr.send(settings.data || null);
    }
}

function send_ordinary_search_query(value) {
    // here we will have to check if the work is in the new bg language or old one
    // currently it is assumed it is in the new bg language

    // send request for the new bg language
    ajax("http://localhost:8081/ordinary_search?query=" + value, {}, handle_ordinary_search_response_new)
    ajax("http://localhost:8081/ordinary_search?query=" + convert(value), {}, handle_ordinary_search_response_old)
}

function send_advanced_search_query(value) {
    // no checks or conversions are done for the advanced search for now
    // maybe think in the future to improve this somehown (wont be easy)

    // send request for the new bg language
    ajax("http://localhost:8081/advanced_search?query=" + value, {}, handle_ordinary_search_response_new)
    ajax("http://localhost:8081/advanced_search?query=" + convert(value), {}, handle_ordinary_search_response_old)
}

function handle_ordinary_search_response_new(response) {
    console.log(response)
    if (response.status == 200 && response.response) {
        var results = JSON.parse(response.response);
        populate(results)
    }
}

function handle_ordinary_search_response_old(response) {
    if (response.status == 200 && response.response) {
        var results = JSON.parse(response.response);
        populateOld(results)
    }
}

function populate(results) {
    var table = document.querySelector("#main-table");
    var tableBody = document.querySelector("#main-table tbody");
    var hits = results.hits.hits

    if (hits.length > 0 && table.classList.contains('non-visible')) {
        table.classList.remove("non-visible");
    }

    for(var i = 0; i < hits.length; i++) {
        var path = hits[i]._source.path
        var snippet = getHighlight(hits[i])

        var tr = document.createElement("tr");
        populateRow(tr, path, snippet, "column1")
        tableBody.appendChild(tr);
    }
}

function populateOld(results) {
    var table = document.querySelector("#main-table");
    var tableBody = document.querySelector("#main-table tbody");
    var hits = results.hits.hits

    if (hits.length > 0 && table.classList.contains('non-visible')) {
        table.classList.remove("non-visible");
    }

    var created_table_rows = tableBody.rows;
    var counter = 0;
    for(; counter < hits.length && counter < created_table_rows.length; counter++) {
        var path = hits[counter]._source.path
        var snippet = getHighlight(hits[counter])

        var tr = created_table_rows[counter];
        populateRow(tr, path, snippet, "column2")
    }

    for(; counter < hits.length; counter++) {
        if (hits[counter].highlight.content.length > 0) {
            var path = hits[counter]._source.path
            var snippet = getHighlight(hits[counter])

            var tr = document.createElement("tr");
            tr.appendChild(document.createElement("td"), ["column1"]);
            populateRow(tr, path, snippet, "column2")
            tableBody.appendChild(tr);
        }
    }
}

function createTD(path, snippet, classes) {
    var col = document.createElement("td");
    col.innerHTML = "<div class=\"file-path\"> <b>Файл: </b>" + path + "</div> <br> <div>" + (snippet != null ? "<b>Откъс: </b>" + snippet : "") + "</div>";
    for (var i = 0; i < classes.length; i++) {
        col.classList.add(classes[i]);
    }

    col.addEventListener("click", function() {
        var path = this.childNodes[0].childNodes[2].data
        // openPdf(path)
    });

    return col;
}

function populateRow(tr, path, snippet, classvalue) {
    tr.appendChild(createTD(path, snippet, [classvalue]));
}

function getHighlight(value) {
    if(value && value.highlight && value.highlight.content[0]) {
        return value.highlight.content[0]
    } else {
        return null
    }
}

