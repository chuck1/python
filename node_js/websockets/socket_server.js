
var net = require("net");

var server = net.createServer(function(socket) {
	//socket.write('Echo server\r\n');

	socket.on('data', (data) => {
		console.log("received", data);
	});

	socket.pipe(socket);
});

server.listen({port:14000, host:'0.0.0.0'}, () => {
	console.log("listening");
});

