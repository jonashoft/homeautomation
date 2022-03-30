var nodeTradfriClient = require("node-tradfri-client");

nodeTradfriClient.discoverGateway().then((result) => console.log(result))
