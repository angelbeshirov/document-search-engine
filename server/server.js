const express = require("express")
const bodyParser = require("body-parser")
const url = require('url');
const elasticsearch = require("elasticsearch")
const fileSystem = require('fs')
const pathModule = require('path');

const app = express()
app.use(bodyParser.json())

app.listen(process.env.PORT || 8081, () => {
    console.log("connected")
})

const client = elasticsearch.Client({
    host: "http://127.0.0.1:9200",
})

// Add headers
app.use(function (req, res, next) {
    res.setHeader('Access-Control-Allow-Origin', 'http://127.0.0.1:8080');
    res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE');
    res.setHeader('Access-Control-Allow-Headers', 'X-Requested-With,content-type');
    res.setHeader('Access-Control-Allow-Credentials', true);
    next();
});

app.get("/ordinary_search", (req, res) => {
    const value = req.query['phrase_new']
    const value1 = req.query['phrase_old']
    const from = req.query['from']
    const size = req.query['size']
    const query = {
        index: "library_index",
        body: {
            _source: ["path"],
            size: size,
            from: from,
            query: {
                bool : {
                    should: [{
                        match_phrase: {
                            "content": value.trim()
                        }
                    }, {
                        match_phrase: {
                            "content": value1.trim()
                        }
                    }]
                }
            },
            highlight: {
                pre_tags: ["<b>"],
                post_tags: ["</b>"],
                order : "score",
                type : "unified",
                fields: {
                    content: {
                        fragment_size : 300,
                        number_of_fragments : 15
                    }
                }
            }
        }
    }
    client.search(query)
    .then(response => {
        return res.json(response)
    })
    .catch(err => {
        return res.status(500).json({"message": "Error"})
    })
})

app.get("/advanced_search", (req, res) => {
    const query_string = req.query['phrase_new']
    const query_string_old = req.query['phrase_old']
    const from = req.query['from']
    const size = req.query['size']

    const query = {
        index: "library_index",
        from: from,
        size: size,
        body: {
            _source: ["path"],
            query: {
                bool : {
                    should: [{
                        query_string: {
                            query: query_string.trim(),
                            default_field: "content"
                        }
                    }, {
                        query_string: {
                            query: query_string_old.trim(),
                            default_field: "content"
                        }
                    }]
                }
            },
            highlight: {
                pre_tags: ["<b>"],
                post_tags: ["</b>"],
                order : "score",
                type : "unified",
                fields: {
                    content: {
                        fragment_size : 300,
                        number_of_fragments : 15
                    }
                }
            }
        }
    }
    client.search(query)
    .then(response => {
        return res.json(response)
    })
    .catch(err => {
        return res.status(500).json({"message": "Error"})
    })
})

app.get("/ordinary_search/count", (req, res) => {
    const value = req.query['phrase_new']
    const value1 = req.query['phrase_old']
    const query = {
        index: "library_index",
        body: {
            query: {
                bool : {
                    should: [{
                        match_phrase: {
                            "content": value.trim()
                        }
                    }, {
                        match_phrase: {
                            "content": value1.trim()
                        }
                    }]
                }
            }
        }
    }
    client.count(query)
    .then(response => {
        return res.json(response)
    })
    .catch(err => {
        return res.status(500).json({"message": "Error"})
    })
})

app.get("/advanced_search/count", (req, res) => {
    const query_string = req.query['phrase_new']
    const query_string_old = req.query['phrase_old']
    const query = {
        index: "library_index",
        body: {
            query: {
                bool : {
                    should: [{
                        query_string: {
                            query: query_string.trim(),
                            default_field: "content"
                        }
                    }, {
                        query_string: {
                            query: query_string_old.trim(),
                            default_field: "content"
                        }
                    }]
                }
            }
        }
    }
    client.count(query)
    .then(response => {
        return res.json(response)
    })
    .catch(err => {
        return res.status(500).json({"message": "Error"})
    })
})

app.get("/open", (req, res) => {
    const path = req.query['path']

    var statistics = fileSystem.statSync(path);

    res.writeHead(200, {
        'Content-Length': statistics.size
    });

    var readStream = fileSystem.createReadStream(path);
    readStream.pipe(res);
})