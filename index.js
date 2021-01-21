const Discord = require('discord.js'); // discord offical API
const Keys = require('./keys.json'); 
const MessageHandler = require('./msg_handler')

const client = new Discord.Client();

client.once('ready', () => {
    console.log("PojzoBot is online!"); // once the bot is online, let the user know
})

client.on('message', msg => { 
    console.log(msg.content);
    var response = MessageHandler.handleMessage(msg, client); // get a reply depending on the message
    if (response === null) return; // if message didnt get approved, do nothing
    msg.reply(response);
})

var token = Keys.token;
client.login(token);