var http = require('http');
const spawn = require('child_process').spawn
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
            getResponseFromInt(JSON.parse(chunk).intent.name, resp)

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
function getResponseFromInt(intentName, response) {

    postBody = JSON.stringify({
        "name": intentName.toString(),
        "entities": {
            "temperature": "high"
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
            // botRes=JSON.parse(chunk).messages;
            //console.log("the bot says: "+ JSON.parse(chunk).messages[0].text )
            console.log("the bot says: " + JSON.parse(chunk).messages[0])
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
    const ls = spawn('python3', ['../asr/asr.py', '../server/audio.wav']);
    ls.stdout.on('data', (data) => {
        console.log(`stdout: ${data}`);
      });
      
      ls.stderr.on('data', (data) => {
        console.log(`stderr: ${data}`);
      });
      
      ls.on('close', (code) => {
        console.log(`child process exited with code ${code}`);
      });
    
}


// Exports module for app.js

module.exports = {
    sendIntent,
    ASR,

}