document.addEventListener('DOMContentLoaded', () => {
    fetchTiendas();
    document.querySelector('#filter-form').addEventListener('submit', (event) => {
        event.preventDefault();
        fetchTiendas();
    });

    const params = new URLSearchParams(window.location.search);
    const mensaje = params.get('mensaje');

    if (mensaje) {
        let messageText = '';
        switch (mensaje) {
            case 'successAddTienda':
                messageText = 'Tienda agregada con éxito!';
                break;
            case 'successModifyTienda':
                messageText = 'Tienda actualizada con éxito!';
                break;
            case 'successDeleteTienda':
                messageText = 'Tienda eliminada con éxito!';
                break;
            default:
                messageText = '';
        }

        if (messageText) {
            console.log("ShowPopUp")
            showPopup(messageText);
        }
    }
});

function showPopup(message) {
    const popup = document.getElementById('popup');
    if (popup) {
        popup.textContent = message;
        popup.classList.add('show');
        setTimeout(() => {
            popup.classList.remove('show');
        }, 3000);
    }
}

function modifyTienda(idTienda) {
    window.location.href = `/modificarTienda?idTienda=${idTienda}`;
}

function deleteTienda(idTienda) {
    fetch('/eliminarTienda', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tiendaId: idTienda })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/tiendas?mensaje=successDeleteTienda';
        } else {
            console.error('Error al eliminar tienda');
        }
    })
    .catch(error => {
        console.error('Error al enviar solicitud de eliminación:', error);
    });
}

function fetchTiendas() {
    const idTienda = encodeURIComponent(document.querySelector('#idTienda-filter').value);
    const habilitado = encodeURIComponent(document.querySelector('#habilitado-filter').value);
    var urlFiltro = ""
    console.log("fetchTiendas 1 + habilitado = " + habilitado)
    if(idTienda || habilitado){
        console.log("fetchTiendas 2 + habilitado = " + habilitado)
        urlFiltro = `/api/tiendas/filtradas?idTienda=${idTienda}&estado=${habilitado}`
    } else {
        urlFiltro = '/api/tiendas'
    } 
    fetch(urlFiltro)
    .then(response => response.json())
    .then(tiendas => {
        const tableBody = document.querySelector('#tiendas-table tbody');
        tableBody.innerHTML = '';

        tiendas.forEach(tienda => {
            console.log(tienda)
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${tienda.idTienda}</td>
                <td>${tienda.direccion}</td>
                <td>${tienda.ciudad}</td>
                <td>${tienda.provincia}</td>
                <td>${tienda.habilitado ? 'Sí' : 'No'}</td>
                <td>
                    <button class="btn-modify" onclick="modifyTienda('${tienda.idTienda}')">Modificar</button>
                    <button class="btn-delete" onclick="deleteTienda('${tienda.idTienda}')">Eliminar</button>
                </td>
            `;

            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de tiendas:', error);
    });
}
