
var allowed_channels = require('../jsons/allowed_channels.json');
var commands = require('./commands.js');
var index = require('./index.js')
var define = require('./functions/define.js');

function filterChannel(msg) {
    if (allowed_channels.channels.includes(msg.channel.name)) return true; // if message is from allowed channel return true
    return false
}

function validMessage(msg, client) {
    if (!msg.content.startsWith("%")) return false; // bot is called with %...
    if (msg.author === client.user.id) return false; // dont read own messages
    if (!filterChannel(msg)) return false; // if message was sent in wrong channel

    return true; // if conditions are met, return true;
}

function stripMessage(message) { // rid content of a message of % at the beginning
    var temp = message.split(/\s+/);
    if (temp.length == 1) { // if its only % and nothing else return null
        return null;
    }
    return temp.slice(1).join(" "); // otherwise join string without the first one (%)
}

function handleFunctionReturns(msg, text) {
    index.sendMessage(msg, text);
}

function handleMessage(msg, client) {
    if (!validMessage(msg, client)) return null; // only continue if message is valid

    var message = stripMessage(msg.content);
    define.primary(msg, message);
    /*
    console.log("got here");
    const spawn = require('child_process').spawn;

    const process = spawn('python', ['../python/predict_response.py', message])

    process.stdout.on('data', data => {
        index.sendMessage(msg, data.toString());
    })
    return null;
    */
   return null;
}

module.exports.handleMessage = handleMessage;
module.exports.handleFunctionReturns = handleFunctionReturns