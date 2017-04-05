var http = require("http");
var express = require("express");

var sys = require('sys')
var exec = require('child_process').exec;
var child;


var call_hello = function() {

	// executes `pwd`
	child = exec("webcam image.jpg", function (error, stdout, stderr) {
		sys.print('stdout: ' + stdout);
		sys.print('stderr: ' + stderr);
		if (error !== null) {
			console.log('exec error: ' + error);
		}
	});

}


http.createServer(function(request, response) {
	response.writeHead(200, {"Content-Type": "text/plain"});
	response.write("Hello World");

	call_hello();

	response.end();
}).listen(8888);
