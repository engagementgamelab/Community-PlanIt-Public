var app = require("express").createServer(),
    prova = require("../../../prova/prova"),
    fs = require("fs"),
    Script = process.binding('evals').Script,
    Mustache = require("../../../mustache.js/mustache.js");

// hello world
app.get("/node", function(req, res){
	res.send("hello world");
});

// output some json!
app.get("/node/json", function(req, res){
	var obj = {
		test: "lol",
		hai: false
	};

	res.send(JSON.stringify(obj));
});

// Test harness
app.get("/node/test", function(req, res) {
    var runner = require("../../test/runner.js");
    //runner.prova.on("finish", function() {
        fs.readFile("../../../prova/demo.html", function(handle, data) {
            var view = {
                title: "prova nodejs unit testing",
                modules: [
                { name: "default", tests: [{ label: "test something", status: true }, { label: "test something else", status: false }, { name: "not default" }]
                }]
            },
            html = Mustache.to_html(data.toString(), view);

            res.send(html);
        });
    //});
});

app.listen(4040);
