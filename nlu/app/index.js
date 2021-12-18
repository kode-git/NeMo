function sendIte() {
    var question = $("#write").val()
    let form = document.getElementById('form1');
    let li2 = document.createElement('p');
    li2.textContent = "you: "+question;
    document.getElementById("write").value=null

// insert a new node before the first list item
form.insertBefore(li2,form.firstChild);

    $.ajax({
        url: "/sendInt",
        type: "POST",
        dataType: "json",
        data: {
            'text' : question 
        },

        success: function (data) {

            let li = document.createElement('p');
            li.textContent = "bot: "+data;

        // insert a new node before the first list item
        form.insertBefore(li,form.firstChild);
                console.log(data)
        }
    });
};