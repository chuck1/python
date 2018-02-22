const WebSocket = require('ws');

const wss = new WebSocket.Server({ host: '192.168.56.2', port: 13000 });

wss.on('connection', function connection(ws) {
	
	console.log("new connection");

	ws.on('message', function incoming(message) {
		      console.log('received: %s', message);
		    });
	
	ws.on('error', function(e) {
		console.log('error', e);
	});

	ws.on('close', function(e) {
		console.log('close');
		console.log(e);
	});

	ws.send('something');
});

