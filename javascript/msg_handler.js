
var allowed_channels = require('../jsons/allowed_channels.json');
var commands = require('./commands.js');

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
function handleMessage(msg, client) {
    if (!validMessage(msg, client)) return null; // only continue if message is valid

    var message = stripMessage(msg.content);
    
    var funcName = commands.getCorrespondingFunction(message); // get corresponding function given the message as input
    if (funcName == null) return "I can't answer this question yet"; // if no match was found, return null
    try { // try to import function using its name
        var func = require("./functions/" + funcName); 
    }
    catch { // file with given function is missing
        console.log("Couldnt find file with corresponding function");
        return null;
    }
    func.primary(message, msg);
    return null;

}

exports.handleMessage = handleMessage;