commands = { // will move this into a new file in the future.
    "hello": "greet",
    "what does": "urban.js"
}



function printAllCommands() { // print all commands and their corresponding functions
    for (var key in commands) { // iterate over all commands
        console.log(`${key} : ${commands[key]}`);
    }
}

function getCorrespondingFunction(message) { // return corresponding function to given input
    console.log(message);
    for(var key in commands) { // iterate over all commands 
        if (message.includes(key)) { // when a match is found, return corresponding function
            return commands[key];
        }
    }
    return null;
}

// exporting variables and function to use them in other modules

module.exports.commands = commands;
module.exports.printAllCommands = printAllCommands;
module.exports.getCorrespondingFunction = getCorrespondingFunction