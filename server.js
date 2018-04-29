const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 10005 });

wss.on('connection', function connection(ws) {
	
	console.log("new connection");

	ws.on('message', function incoming(message) {
		      console.log('received: %s', message);
		    });
	
	ws.on('error', function(e) {
		console.log('error', e);
	});

	ws.on('close', function(e) {
		console.log('close', e);
	});

	ws.send('something');
});

