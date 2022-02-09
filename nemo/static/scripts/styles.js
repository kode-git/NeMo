// This script changes the content of the chat

var username = "Alysia"
var avatarBot = "bot"
var avatarUser = "user"

// Propagate a message of a player
function insertBotMessage(username, message){
    var contentChat = document.getElementById('content-chat')
    var tag = document.createElement('div') // right-msg div
    // adding class to tag
    tag.classList.add('msg')
    tag.classList.add('left-msg')
    var avatarContent = document.createElement('div') // avatar div
    avatarContent.classList.add('msg-img')
    avatarContent.style.backgroundImage = "url(static/avatars/" + avatarBot +".png)"
    var bubble = document.createElement('div') // msg-bubble div
    bubble.classList.add('msg-bubble')

    var messageContent = document.createElement('div') // msg-text
    messageContent.classList.add('msg-text')
    var text = document.createTextNode(username  + ": " + message)
    messageContent.appendChild(text)
    bubble.appendChild(messageContent)
    tag.appendChild(avatarContent) // Avatar before the bubble
    tag.appendChild(bubble) // Bubble after the avatar
    contentChat.appendChild(tag)
    contentChat.scrollTop = contentChat.scrollHeight;
}


// This function is to put an own message in the chat
function insertMessage(message) {
    var contentChat = document.getElementById('content-chat')
    var tag = document.createElement('div') // right-msg div
    // adding class to tag
    tag.classList.add('msg')
    tag.classList.add('right-msg')
    var avatar = document.createElement('div') // avatar div
    avatar.classList.add('msg-img')
    avatar.style.backgroundImage = "url(static/avatars/" + avatarUser +".png)"
    var bubble = document.createElement('div') // msg-bubble div
    bubble.classList.add('msg-bubble')

    var messageContent = document.createElement('div') // msg-text
    messageContent.classList.add('msg-text')
    var text = document.createTextNode("You: " + message)
    messageContent.appendChild(text)
    bubble.appendChild(messageContent)
    tag.appendChild(avatar) // Avatar before the bubble
    tag.appendChild(bubble) // Bubble after the avatar
    contentChat.appendChild(tag)
    contentChat.scrollTop = contentChat.scrollHeight;
}