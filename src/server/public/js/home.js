document.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const usuario = urlParams.get('usuario');
    const mensaje = urlParams.get('mensaje');

    if (usuario) {
        document.getElementById('welcome-message').textContent = `Bienvenido, ${decodeURIComponent(usuario)}!`;
    }
});
