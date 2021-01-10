#!/usr/bin/env node

var ws_module = require('ws');
var net = require('net');

var wsMask = (argv.method == 'tcp2ws');

function initSocketCallbacks(state,ws,s) {

	function flushSocketBuffer() {
		if(state.sBuffer.length > 0) {
			s.write(Buffer.concat(state.sBuffer));
		}
		state.sBuffer = null;
	};

	function flushWebsocketBuffer() {
		if(state.wsBuffer.length > 0) {
			ws.send(Buffer.concat(state.wsBuffer),{binary: true,mask: wsMask});
		}
		state.wsBuffer = null;
	};

	s.on('close', function(had_error) {
		ws.removeAllListeners('close');		
		ws.close();
	});

	ws.on('close', function() {
		s.removeAllListeners('close');	
		s.end();
	});

	ws.on('error', function (e) {
		console.log('websocket error');
		console.log(e);
		ws.removeAllListeners('close');
		s.removeAllListeners('close');
		ws.close();
		s.end();
	});

	s.on('error', function (e) {
		console.log('socket error');
		console.log(e);
		ws.removeAllListeners('close');
		s.removeAllListeners('close');
		ws.close();
		s.end();
	});

	s.on('connect', function() {
		state.sReady = true;
		flushSocketBuffer();
	});

	ws.on('open', function () {
		state.wsReady = true;
		flushWebsocketBuffer();
	});

	s.on('data', function(data) {

		if(! state.wsReady) {
			state.wsBuffer.push(data);
		} else {
			ws.send(data,{binary: true,mask: wsMask});
		}
	});

	ws.on('message', function(m,flags) {
		if(!state.sReady) {
			state.sBuffer.push(m);
		} else {
			s.write(m);			
		}
	});
}

function tcp2ws() {
	console.log('proxy mode tcp -> ws');
	console.log('forwarding port ' + argv.lport + ' to ' + argv.rhost);

	var server = net.createServer(function(s) {
		var ws = new ws_module(argv.rhost);
		
		var state = {
			sReady : true,
			wsReady : false,
			wsBuffer: [],
			sBuffer : []
		};
		initSocketCallbacks(state,ws,s);
	});
	server.listen(argv.lport);
}

