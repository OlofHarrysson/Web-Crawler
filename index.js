var express = require("express");
var throttle = require("express-throttle");
var Chance = require('chance');
var chance = new Chance();
var _ = require("underscore");
  
var userAgent = function (req, res, next) {
  if(req.headers["user-agent"]==="DDW" || req.headers["user-agent"].indexOf("Mozilla")!=-1 ){
  	next();	
  } else {
  	res.status(400).send("User agent "+req.headers["user-agent"]+" not allowed!");
  }  
};

var app = express();
app.use(express.static('./'));
app.use(userAgent);
app.use(throttle({ "rate": "1/s" }));

var port = 8000;

var cities = _.range(100).map(function () { return chance.city(); });
var persons = _.range(500).map(function () { return chance.name(); });
 
app.get("/", function(req, res, next) {
	var content = "<h1>Cities:</h1>";
	content += "<ul class=\"cities\">";
	content += _.sample(cities,10).map(function(city) {
		return "<li><a href=\"/city/"+city+"\">"+city+"</a></li>";
	}).join("");
	content += "</ul>";
	res.send(content);
});

app.get("/city/:city", function(req, res, next) {
	var content = "<h1>"+req.params.city+"</h1>";
	content += "<h3>Persons:</h3>";
	content += "<ul class=\"persons\">";
	content += _.sample(persons,5).map(function(person) {
		return "<li><a href=\"/person/"+person+"\">"+person+"</a></li>";
	}).join("");
	content += "</ul>";

	content += "<h3>Other cities:</h3>";
	content += "<ul class=\"cities\">";
	content += _.sample(cities,3).map(function(city) {
		return "<li><a href=\"/city/"+city+"\">"+city+"</a></li>";
	}).join("");
	content += "</ul>";
	res.send(content);
});

app.get("/person/:person", function(req, res, next) {
	var content = "<h1>"+req.params.person+"</h1>";
	content += "<div class=\"person\">";
	content += "<span class=\"name\">"+req.params.person+"</span><br />";	
	content += "<span class=\"phone\">"+chance.phone()+"</span><br />";	
	content += "<span class=\"gender\">"+chance.gender()+"</span><br />";	
	content += "<span class=\"age\">"+chance.age()+"</span><br />";	
	content += "</div>";

	content += "<h3>Other cities:</h3>";
	content += "<ul class=\"cities\">";
	content += _.sample(cities,3).map(function(city) {
		return "<li><a href=\"/city/"+city+"\">"+city+"</a></li>";
	}).join("");
	content += "</ul>";
	res.send(content);
});

app.listen(port, function () {
  console.log('App listening on port '+port);
});