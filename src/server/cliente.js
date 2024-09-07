const path = require('path');
const session = require('express-session');

const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));

const usuarioController = require('./controllers/usuarioController');

app.use(session({
  secret: 'tp-grpc',
  resave: false,
  saveUninitialized: true,
}));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'login.html'));
});

app.post('/login', usuarioController.iniciarSesion);

app.get('/home', (req, res) => {
  if (req.session.authenticated) {
    const usuario = encodeURIComponent(req.session.usuario);
    res.redirect(`/home.html?usuario=${usuario}`);
  } else {
    res.redirect('/');
  }
});

app.get('/crearUsuario', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'crearUsuario.html'));
  } else {
    res.redirect('/');
  }
});

app.post('/crearUsuario', usuarioController.crearUsuario);

app.get('/logout', usuarioController.cerrarSesion);

app.get('/usuarios', (req, res) => {
  if (req.session.authenticated) {
    res.sendFile(path.join(__dirname, 'public', 'usuarios.html'));
  } else {
    res.redirect('/');
  }
});

app.get('/api/usuarios', usuarioController.traerUsuarios);

app.get('/usuario/:idUsuario', usuarioController.mostrarUsuario);

app.post('/modificarUsuario', usuarioController.modificarUsuario);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Servidor web ejecutándose en http://localhost:${PORT}`);
});
