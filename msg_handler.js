
var allowed_channels = require('./allowed_channels.json');

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
    return temp.slice(1).join(); // otherwise join string without the first one (%)
}

function handleMessage(msg, client) {
    if (!validMessage(msg, client)) return null; // only continue if message is valid

    var content = stripMessage(msg.content);
    if (content === null) return content;

    if (content.toLowerCase() == "hello") {
        return "Hello";
    }
    return null;
}

exports.handleMessage = handleMessage;