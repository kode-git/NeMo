var http = require('http');
const spawnSync = require('child_process').spawnSync
var botResponse = ""

//predictor of the interested intent
function sendIntPost(data, resp) {
    postBody = JSON.stringify({
        'text': data.text
    });
    const options = {
        hostname: 'localhost',
        port: 5005,
        path: '/model/parse',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postBody, 'utf8')
        }
    }
    // create request
    const req = http.request(options, res => {

        res.setEncoding('utf8');
        res.on('data', function (chunk) {
            console.log("the user says: " + JSON.parse(postBody).text)
            console.log("the intent predicted is: " + JSON.parse(chunk).intent.name + " with a confidence of " +
                JSON.parse(chunk).intent.confidence);
                console.log("the entity is: "+JSON.parse(chunk).entities[0].value);
                entityType=JSON.parse(chunk).entities[0].entity;
                entityValue=JSON.parse(chunk).entities[0].value;
            getResponseFromInt(JSON.parse(chunk).intent.name, resp,entityType,entityValue)

        });
    })

    // managing in case of error
    req.on('error', error => {
        console.error(error)
    })

    // write data in the request
    req.write(postBody)
    // send and close channel
    req.end()
}

// getting the response given the best predicted intent
function getResponseFromInt(intentName, response,myEntityType,myEntityValue) {
    

    postBody = JSON.stringify({
        "name": intentName.toString(),
        "entities": {
            myEntityType: myEntityValue
        }
    });

    const options = {
        hostname: 'localhost',
        port: 5005,
        path: '/conversations/default/trigger_intent',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postBody, 'utf8')
        }
    }
    // create request

    const req = http.request(options, res => {

        res.setEncoding('utf8');
        res.on('data', function (chunk) {
            console.log("Jarvis says: " + JSON.parse(chunk).messages[0])
            botResponse = JSON.parse(chunk).messages[0].text
            response.status(200).json(botResponse)
        });
    })

    // managing in case of error
    req.on('error', error => {
        console.error(error)
    })

    // write data in the request
    req.write(postBody)
    // send and close channel
    req.end()


}

const sendIntent = (request, response) => {
    sendIntPost(request.body, response)
    //response.status(200).json(botResponse)

}

const ASR = (request, response) =>{
    var ls = spawnSync('python3', ['../asr/asr.py', '../server/audio.wav']);
    out = ls.stdout + "";
    // parsing the string and extract the output
    var parsed = out.substring(
        out.indexOf("@\n[") + 4,
        out.lastIndexOf("]\n@") - 1
     );
    return parsed
}


// Exports module for server.js

module.exports = {
    sendIntent,
    ASR,

}