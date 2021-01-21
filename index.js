const Discord = require('discord.js');
const keys = require('./keys.json');

const client = new Discord.Client();

client.once('ready', () => {
    console.log("PojzoBot is online!");
})

var token = keys.token;
client.login(token);