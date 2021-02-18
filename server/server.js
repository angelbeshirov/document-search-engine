const express = require("express")
const bodyParser = require("body-parser")
const url = require('url');
const elasticsearch = require("elasticsearch")
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
    const value = req.query['query']
    client.search({
        index: "library_index",
        
        body: {
            _source: ["path"],
            size: 10000,
            query: {
                match_phrase: {"content": value.trim()}
            },
            highlight: {
                pre_tags: ["<b>"],
                post_tags: ["</b>"],
                order : "score",
                type : "unified",
                fields: {
                    content: {
                        fragment_size : 0,
                        number_of_fragments : 10
                    }
                }
            }
        }
    })
    .then(response => {
        return res.json(response)
    })
    .catch(err => {
        return res.status(500).json({"message": "Error"})
    })
})

app.get("/advanced_search", (req, res) => {
    const query_string = req.query['query']
    client.search({
        index: "library_index",
        size: 10000,
        body: {
            _source: ["path"],
            query: {
                query_string: {
                    query: query_string.trim(),
                    default_field: "content"
                }
            },
            highlight: {
                pre_tags: ["<b>"],
                post_tags: ["</b>"],
                order : "score",
                type : "unified",
                fields: {
                    content: {
                        fragment_size : 0,
                        number_of_fragments : 10
                    }
                }
            }
        }
    })
    .then(response => {
        return res.json(response)
    })
    .catch(err => {
        return res.status(500).json({"message": "Error"})
    })
})