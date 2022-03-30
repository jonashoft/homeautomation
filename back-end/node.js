"use strict";

const express = require("express");
const http = require("http");
const WebSocket = require("ws"); 
var Gpio = require('onoff').Gpio;

var socketOne = new Gpio(23, 'out');
var socketTwo = new Gpio(24, 'out');

const app = express();
const server = http.createServer(app);
const websocketServer = new WebSocket.Server({ server });

websocketServer.on("connection", (webSocketClient) => {
    webSocketClient.on('message', function message(data) {
        let parsedData = JSON.parse(data);
        // if (parsedData.hasOwnProperty('roomState')){
        //     console.log("room: %s", parsedData['roomState'])
        // }
        // if (parsedData.hasOwnProperty('roomValue')){
        //     console.log("room: %s", parsedData['roomValue']);
        // }
        // if (parsedData.hasOwnProperty('toiletState')){
        //     console.log("toilet: %s", parsedData['toiletState'])
        // }
        // if (parsedData.hasOwnProperty('toiletValue')){
        //     console.log("toilet: %s", parsedData['toiletValue'])
        // }
        // if (parsedData.hasOwnProperty('hallState')){
        //     console.log("hall: %s", parsedData['hallState'])
        // }
        // if (parsedData.hasOwnProperty('hallValue')){
        //     console.log("hall: %s", parsedData['hallValue'])
        // }
        if (parsedData.hasOwnProperty('chainState')){
            let state = parsedData['chainState'];
            console.log("chain: %s", state)
            console.log("socket1: %s", socketOne.readSync());
            console.log("socket2: %s", socketTwo.readSync());
            if (Boolean(socketOne.readSync()) != state){
                console.log("here")
                socketOne.writeSync(state)
            }
            if (Boolean(socketTwo.readSync()) != state){
                socketTwo.writeSync(state)
            }
        }
      });
    setInterval(() => {
        let socketOneState = Boolean(socketOne.readSync());
        let socketTwoState = Boolean(socketTwo.readSync());

        let dataObj = {
            chainState: socketOneState
        }
        webSocketClient.send(JSON.stringify(dataObj));
    }, 5000);
});

server.listen(3000, () => {
  console.log("Websocket server started on port 3000");
});