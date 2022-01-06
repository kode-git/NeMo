
// TODO MediaRecord management


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


function sendRecord(){
    // TODO
}
