const express = require('express')
const app = express()
const ejs = require('ejs')
const mongoose = require('mongoose')
const expressSession = require('express-session')
const flash = require('connect-flash')

// connect mongon
mongoose.connect('mongodb+srv://Rachanov:WAQdj64jHzSNt8aX@cluster0.np6iu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0', {
    // useNewUrlParser: true
})

// Controller
const indexController = require('./controllers/indexController')
const loginController = require('./controllers/loginController')
const registerController = require('./controllers/registerController')

app.use(express.static('public'))
app.use(express.json())
app.use(express.urlencoded())
app.use(flash())
app.set('view engine', 'ejs')

app.get('/', indexController)
app.get('/login', loginController)
app.get('/register', registerController)

app.listen(4000, () => {
    console.log("App listening on port 4000")
})