
// TODO MediaRecord management

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
                    'type': 'audio/mp3' 
                  });
                sendRecord(audioBlob)
                // const audioUrl = URL.createObjectURL(audioBlob);
                // const audio = new Audio(audioUrl);
                // sendRecord(audio)
            });

        });

}

function stopRecord() {
    // delay of 1 second
    setTimeout(() => {
        mediaRecorder.stop();
    }, 1000);
}

function sendRecord(audio) {
    var question = ""
    const formData = new FormData();
    formData.append('audio-file', audio);
    $.ajax({
        url: "/translateQuestion",
        type: "POST",
        body: formData,
        success: function (data) {
            question = data
            let li = document.createElement('p');
            li.textContent = " User : " + data;

            // insert a new node before the first list item
            form.insertBefore(li, form.firstChild);
            console.log(data)
        }
    });

    // Needs to complete with the rasa management with the invocation of the sendMessage
    // the question is in the variable setted at 79 and declared to 71
}

function questionASR(){
    
}
