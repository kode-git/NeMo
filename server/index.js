

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
    var form    = new FormData();
    console.log('Appending...')
    form.append("file", file);
    console.log('Start fetching...')
    fetch('http://localhost:4000/sendAudioQuest', {
    method: 'post',
    body: form,
    })
    .then((res) => console.log(res))
    .catch((err) => ('Error occurred', err))




    // send AudioBlob to speechToText call
    // fd = new FormData()
    // fd.append('blob-name', 'audio.wav')
    // fd.append('data', audioBlob)
    // $.ajax({
    //     url: "/sendIntent",
    //     type: "POST",
    //     dataType: "json",
    //     data: {
    //         'audio': fd
    //     },

    //     success: function (data) {
    //         console.log(data)
    //         // receive response text
    //         // send text to the rasa invocation (sendMessage)
    //         // receive response
    //         // send text to the textToSpeech call
    //         // receive speech audio
    //         // reproduce audio and trascript the message
    //     }
    // });
    // receive response text
    // send text to the rasa invocation (sendMessage)
    // receive response
    // send text to the textToSpeech call
    // receive speech audio
    // reproduce audio and trascript the message
}

function questionASR(){
    
}
