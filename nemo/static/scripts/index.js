
// Buttons for event handlers
const sendButton = document.getElementById('send-chat')
const recordButton = document.getElementById('record-chat')
const stopButton = document.getElementById('stop-chat')

sendButton.addEventListener('click', sendMessage)
recordButton.addEventListener('click', startRecord)
stopButton.addEventListener('click', stopRecord)

// initial state of the stopButton is "none" because the user didn't record by default
stopButton.style.display = "none"

// MediaRecorder
var mediaRecorder;

// Temporal variables
var audioName = 0;
var speechName = 0;

// This function send a request with a question to the NLU rasa module and receive his response
function sendMessage(){
    // Getting the value from the chat field
    var question = document.getElementById("input-chat").value
    document.getElementById("input-chat").value = null
    // insert a new node before the first list item
    console.log('Question: ' + question)
    insertMessage(question)
    // make an AJAX call to make a response from the NLU rasa module
    var quest = {'text': question}
    $.ajax({
        url: "/intent", // call API
        type: "POST",  // POST method available
        contentType: "application/json", // json formatting data
        data: JSON.stringify(quest),
        success: function (data) {
            // the response is the answer of the question based on the most confident intent
            if(data == "" || data == " " || data == undefined) {
                console.log('Not response...') // if the rasa have internal error
            } 
            else insertBotMessage("Alysia", data)
        }
    });
}

// This function start the recording 
function startRecord() {
    stopButton.style.display = "block"
    recordButton.style.display = "none"
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.start();

            const audioChunks = [];

            mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });


            mediaRecorder.addEventListener("stop", () => {
                const audioBlob = new Blob(audioChunks, { 
                    'type': 'audio/wav' 
                  });
                const audioUrl = URL.createObjectURL(audioBlob);
                
                const audio = new Audio(audioUrl);
                // sending the blob to the server
                sendRecord(audioBlob)
            });

        });
}

function stopRecord() {
    stopButton.style.display = "none"
    recordButton.style.display = "block"
    // delay of 1 second
    setTimeout(() => {
        mediaRecorder.stop();
    }, 1000);
}

function sendRecord(blob){
    var filename = audioName + ".wav"
    audioName++;
    var formData = new FormData();
    formData.append("file", blob, "file")
    formData.append("name", filename)

    fetch('http://127.0.0.1:4000/asr', {
        method: 'POST',
        body: formData,

    }).then(response => response.json().then(data =>{
        const message = data['transcript']
        insertMessage(message)
        getResponse(message)
    }))
}


function getResponse(question){
    var quest = {'text': question}
    $.ajax({
        url: "/intent", // call API
        type: "POST",  // POST method available
        contentType: "application/json", // json formatting data
        data: JSON.stringify(quest),
        success: function (data) {
            // the response is the answer of the question based on the most confident intent
            if(data == "" || data == " " || data == undefined) {
                console.log('Not response...') // if the rasa have internal error
            } 
            else{
                // generateAudio(data)
                insertBotMessage("Alysia", data)  
            }
        }
    });
}


function generateAudio(message){
    const filename = speechName + ""
    speechName++;
    const inputText = {'text': message, 'filename' : filename}
    $.ajax({
        url: "/tts", // call API
        type: "POST",  // POST method available
        contentType: "application/json", // json formatting data
        data: JSON.stringify(inputText),
        success: function (data) {
            // the response is the answer of the question based on the most confident intent
            if(data == undefined) {
                console.log('Not audio making...') // if the rasa have internal error
            } 
            else{
                insertBotMessage("Alysia", message)                
            }
        }
    });
}
