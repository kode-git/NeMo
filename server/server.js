const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const route = require('./route')
const path = require('path');
const cors = require('cors')
const multer = require('multer')

const storage = multer.diskStorage({
  filename: function (req, file, cb) {
    console.log('Storing status: OK (200)')
    cb(null, file.originalname)
  },
  destination: function (req, file, cb) {
    console.log('Storaging...')
    cb(null, './')
  },
})

const upload = multer({ storage })

const port = 4000

app.use(bodyParser.json())
app.use(cors())
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


app.post('/sendAudioQuest', upload.single('file'), (req, res) => {
  console.log('Sending Audio Quest to ASR...')
  // invocation of ASR
  route.ASR(req, res)
})



app.post('/sendIntent', route.sendIntent)

// default listening on port ${port}(4000)
app.listen(port, () => {
  console.log(`Log: Backend Server running on port ${port}.`)
  console.log(`Log: Waiting a request...`)
})

