const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const route = require('./route')
const path = require('path');
const port = 4000

app.use(bodyParser.json())
app.use(
    bodyParser.urlencoded({
        extended: true,
    })
)
app.get('/', (request, response) => {
    response.sendFile(path.join(__dirname, 'index.html'));
})

app.get('/script', (request, response) => {
    response.sendFile(path.join(__dirname, 'index.js'));
})

app.post('/sendInt',route.sendIntent)

// default listening
app.listen(port, () => {
    console.log(`Log: Backend Server running on port ${port}.`)
    console.log(`Log: Waiting a request...`)
})

