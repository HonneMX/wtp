'use strict';

const express = require('express');


// константы
const PORT = 3000;
const HOST = '0.0.0.0';

// приложение
const app = express();

// set the view engine to ejs
app.set('view engine', 'ejs');

// index page
app.get('/', function (req, res) {
  res.render('pages/index');
});

// get usersJSON
app.get('/getUsers', function (req, res) {
  res.render('pages/getUsers');
});

// post usersJSON
app.get('/postUser', function (req, res) {
  res.render('pages/postUser');
});

// get token page
app.get('/getToken', function (req, res) {
  res.render('pages/getToken');
});

// Put
app.get('/putPatchUser', function (req, res) {
  res.render('pages/putPatchUser');
});

// Delete user
app.get('/deleteUser', function (req, res) {
  res.render('pages/deleteUser');
});



app.listen(PORT, HOST, () => {
  console.log(`Running on http://${HOST}:${PORT}`);
});