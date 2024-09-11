
const urlParams = new URLSearchParams(window.location.search);
const idUsuario = urlParams.get('idUsuario');

function mostrarDetallesUsuario(usuario) {
    const userDetails = document.getElementById('user-details');
    userDetails.innerHTML = `
        <p><strong>ID:</strong> ${usuario.idUsuario}</p>
        <p><strong>Usuario:</strong> ${usuario.usuario}</p>
        <p><strong>Nombre:</strong> ${usuario.nombre}</p>
        <p><strong>Apellido:</strong> ${usuario.apellido}</p>
        <p><strong>Habilitado:</strong> ${usuario.habilitado ? 'Sí' : 'No'}</p>
        <p><strong>Casa Central:</strong> ${usuario.casaCentral ? 'Sí' : 'No'}</p>
        <p><strong>Tienda:</strong> ${usuario.idTienda}</p>
        <a href="/modificarUsuario?usuario=${usuario.usuario}">Modificar Usuario</a>
    `;
}

fetch(`/usuario/${idUsuario}`)
    .then(response => response.json())
    .then(usuario => mostrarDetallesUsuario(usuario))
    .catch(error => {
        console.error('Error al cargar los detalles del usuario:', error);
        document.getElementById('user-details').innerText = 'Error al cargar los detalles del usuario.';
    });
