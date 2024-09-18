const urlParams = new URLSearchParams(window.location.search);
const idTienda = urlParams.get('idTienda');

function mostrarDetallesTienda(tienda) {
    const userDetails = document.getElementById('user-details');
    userDetails.innerHTML = `
        <p><strong>ID:</strong> ${tienda.idTienda}</p>
        <p><strong>Direccion:</strong> ${tienda.direccion}</p>
        <p><strong>Ciudad:</strong> ${tienda.ciudad}</p>
        <p><strong>Provincia:</strong> ${tienda.provincia}</p>
        <p><strong>Habilitado:</strong> ${tienda.habilitado ? 'Sí' : 'No'}</p>
        <a href="/modificarTienda?tienda=${tienda.tienda}">Modificar Tienda</a>
    `;
}

fetch(`/tienda/${idTienda}`)
    .then(response => response.json())
    .then(tienda => mostrarDetallesTienda(tienda))
    .catch(error => {
        console.error('Error al cargar los detalles de la tienda:', error);
        document.getElementById('user-details').innerText = 'Error al cargar los detalles de la tienda.';
    });
