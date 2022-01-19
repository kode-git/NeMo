

// MediaRecorder
var mediaRecorder;

function sendMessage() {
    var question = $("#write").val()
    let form = document.getElementById('chat');
    let li2 = document.createElement('p');
    li2.textContent = "User : " + question;
    document.getElementById("write").value = null

    // insert a new node before the first list item
    form.insertBefore(li2, form.firstChild);

    $.ajax({
        url: "/sendIntent",
        type: "POST",
        dataType: "json",
        data: {
            'text': question
        },

        success: function (data) {
            let li = document.createElement('p');
            li.textContent = " Jarvis : " + data;

            // insert a new node before the first list item
            form.insertBefore(li, form.firstChild);
            console.log(data)
        }
    });
};

function startRecord() {

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
                sendRecord(audioBlob)
            });

        });

}

function stopRecord() {
    // delay of 1 second
    setTimeout(() => {
        mediaRecorder.stop();
    }, 1000);
}


function sendRecord(blob) {

    // send AudioBlob to speechToText call
    console.log('File making...')
    var file = new File([ blob ], "audio.wav");   
    console.log('Compact in a FormData...')   
    var formInput  = new FormData();
    console.log('Appending...')
    formInput.append("file", file);
    console.log('Start fetching...')
    var message = ""
    fetch('http://localhost:4000/sendAudioQuest', {
    method: 'post',
    body: formInput,
    })
    .then((res) => res.json())
    .then((jsonRes)=>{
        console.log('Response received')
        message = jsonRes.Message
        console.log(jsonRes.Message)
        let form = document.getElementById('chat');
    let li = document.createElement('p');
    li.textContent = " User : " + message;

    // insert a new node before the first list item
    form.insertBefore(li, form.firstChild);
    console.log("Insert " + message + " in the chat as the user question...")

    // sending the message to rasa
    $.ajax({
        url: "/sendIntent",
        type: "POST",
        dataType: "json",
        data: {
            'text': message
        },

        success: function (data) {
            text = data
            if(text == "" || text == " " || text == undefined) text = "I didn't understand, can you repeat?"
            console.log("Data from rasa:" + text)
            $.ajax({
                url: "/sendResponseAudio",
                type: "POST",
                dataType: "json",
                data: {
                    'text': text
                },
        
                success: function (data) {
                    console.log("Audio: " + data.audio_file)
                    let li = document.createElement('p');
                    li.textContent = " Jarvis : " + text;
        
                    // insert a new node before the first list item
                    form.insertBefore(li, form.firstChild);
                }
            });
            
        }
    });

    // reproduce audio and write the message
    })
    .catch((err) => ('Error occurred', err))

}
