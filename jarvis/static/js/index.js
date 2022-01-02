var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext = new AudioContext;

//new audio context to help us record 
var recordButton = document.getElementById("record");
var stopButton = document.getElementById("stop");

//add events to those 3 buttons 
recordButton.addEventListener("click", startRecording);
stopButton.addEventListener("click", stopRecording);



function sendMessage() {
    var question = $("#write").val()
    let form = document.getElementById('chat');
    let li2 = document.createElement('p');
    li2.textContent = "You : " + question;
    document.getElementById("write").value = null

    // insert a new node before the first list item
    form.insertBefore(li2, form.firstChild);
    $.ajax({
        url: "../sendMessage/",
        type: "post",
        dataType: "json",
        data: {
            'text': question
        },
        success: function (data) {
            console.log('Sending..')
            let li = document.createElement('p');
            li.textContent = "Jarvis : " + data;

            // insert a new node before the first list item
            form.insertBefore(li, form.firstChild);
            console.log(data)
        }
    });
};

/**
 *  Trigger audio input and send in Ajax request to Django
 */
function sendRecord(){

}


/**
 * Function to start the record stream
 */
function startRecording(){

}
/**
 * Function to stop the record stream
 */
function stopRecording(){

}

console.log('Log: Entering in the index.js script...')
console.log('Log: Adding buttons...')
