 
var request = require('request');
var index = require('../msg_handler.js');

var url = "https://api.dictionaryapi.dev/api/v2/entries/en/"

const getData = (msg, word) => {
	request(`${url}/${word}`, {json : true}, (err, response, body) => {
		if (!err && response.statusCode === 200) {
			callback(msg, response, body);
		}
	})	
}

const callback = (msg, res, body) => {
	var body = JSON.parse(JSON.stringify(body))[0];
	index.handleFunctionReturns(msg, body['meanings'][0]['definitions'][0]['definition'])
}

module.exports.primary = getData;
