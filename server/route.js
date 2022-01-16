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
            getResponseFromInt(JSON.parse(chunk).intent.name, resp,JSON.parse(chunk).entities)

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
function getResponseFromInt(intentName, response,entities) {


    postBody = {
        "name": intentName.toString(),
        "entities": {}
    }

    //filling the json body with the entities 
    entities.forEach(element => postBody.entities[element.entity] = element.value)
    postBodyString = JSON.stringify(postBody)



    const options = {
        hostname: 'localhost',
        port: 5005,
        path: '/conversations/default/trigger_intent',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postBodyString, 'utf8')
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
    req.write(postBodyString)
    // send and close channel
    req.end()


}

const sendIntent = (request, response) => {
    sendIntPost(request.body, response)
}

const ASR = async function(request, response){
    console.log('Called ASR method in route.js..')
    responseData = ""
    const options = {
        hostname: '127.0.0.1',
        port: 9000,
        path: '/asr/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength('{}', 'utf8')
        }
    }
    // create request
    const req = http.request(options, res => {
        res.setEncoding('utf8');
        res.on('data', function (data) {
            data = JSON.parse(data)
            responseData = data.text[0]
            response.status(200).json({ "Message": responseData })
        });
    })
    
    req.write('{}')
    req.end()

}


const TTS = async function(request, response){
    console.log("Received TTS request :" + request.body)
    postBody = JSON.stringify({
        'text': request.body.text
    });

    console.log('Called ASR method in route.js..')
    responseData = ""
    const options = {
        hostname: '127.0.0.1',
        port: 9000,
        path: '/tts/',
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postBody, 'utf8')
        }
    }
    // create request
    const req = http.request(options, res => {
        res.setEncoding('utf8');
        res.on('data', function (data) {
            data = JSON.parse(data)
            responseAudio = data.audio_file
            response.status(200).json({"audio_file" : responseAudio })
        });
    })
    
    req.write(postBody)
    req.end()

}




// Exports module for server.js

module.exports = {
    sendIntent, // Text message full management
    ASR, // question management in audio mode
    TTS, // response management in audio and text mode
}