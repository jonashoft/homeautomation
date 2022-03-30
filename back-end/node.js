"use strict";

const express = require("express");
const http = require("http");
const WebSocket = require("ws"); 
var Gpio = require('onoff').Gpio;

var socketOne = new Gpio(11, 'out');
var socketTwo = new Gpio(13, 'out');

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
            console.log("chain: %s", state)

            let state = parsedData['chainState'];
            
            if (socketOne.readSync() != state){
                socketOne.writeSync(state)
            }
            if (socketTwo.readSync() != state){
                socketTwo.writeSync(state)
            }
        }
      });
    setInterval(() => {
        let socketOne = Boolean(socketOne.readSync());
        let socketTwo = Boolean(socketTwo.readSync());
        let dataObj = {
        //   roomState: false,
        //   roomValue: 50,
        //   toiletState: false,
        //   toiletValue: 14,
        //   hallState: true,
        //   hallValue: 89,
            chainState: socketOne
        }
        webSocketClient.send(JSON.stringify(dataObj));
    }, 5000);
});

server.listen(3000, () => {
  console.log("Websocket server started on port 3000");
});