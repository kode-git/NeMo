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

app.get('/index.js', (request, response) => {
    response.sendFile(path.join(__dirname, 'index.js'));
})

app.post('/translateQuestion', route.translateQuestion)

app.post('/sendIntent',route.sendIntent )

// default listening on port ${port}(4000)
app.listen(port, () => {
    console.log(`Log: Backend Server running on port ${port}.`)
    console.log(`Log: Waiting a request...`)
})

