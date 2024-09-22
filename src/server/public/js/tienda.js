document.addEventListener('DOMContentLoaded', () => {
    fetchTiendas();
    /*document.getElementById('createTiendaForm').addEventListener('submit', handleSubmit);*/
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
        body: JSON.stringify({ idTienda: idTienda })
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
        const divHtml = document.querySelector('#rellenarTiendas');
        divHtml.innerHTML = "";
        tiendas.forEach((tienda, index) => {
            var nuevaDiv = `
            <div class="container col${1 + (index % 2)}">
                <div class="box c1 bordeR">${tienda.idTienda}</div>
                <div class="box c2">${tienda.direccion}</div>
                <div class="box c3">${tienda.ciudad}</div>
                <div class="box c4 bordeR">${tienda.provincia}</div>
                <div class="box c5 ">${tienda.habilitado ? 'Sí' : 'No'}</div>       
                <div class="box c6">
                    <button class="btn-modify" onclick="modifyTienda('${tienda.idTienda}')">Modificar</button>
                    <button class="btn-delete" onclick="deleteTienda('${tienda.idTienda}')">Eliminar</button>
                </div>
            </div>
            `;
            if(index === tiendas.length - 1){
                nuevaDiv = `
                <div class="container col${1 + (index % 2)}">
                    <div class="box c1 bordeB bordeR">${tienda.idTienda}</div>
                    <div class="box c2 bordeB">${tienda.direccion}</div>
                    <div class="box c3 bordeB">${tienda.ciudad}</div>
                    <div class="box c4 bordeB bordeR">${tienda.provincia}</div>
                    <div class="box c5 bordeB">${tienda.habilitado ? 'Sí' : 'No'}</div>       
                    <div class="box c6 bordeB">
                        <button class="btn-modify" onclick="modifyTienda('${tienda.idTienda}')">Modificar</button>
                        <button class="btn-delete" onclick="deleteTienda('${tienda.idTienda}')">Eliminar</button>
                    </div>
                </div>
                `;
            }
            divHtml.innerHTML += nuevaDiv;
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de tiendas:', error);
    });
}



async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = new URLSearchParams(formData).toString();
    
    try {
        const response = await fetch('/crearTienda', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

        const result = await response.text();
        
        if (response.status === 400) {
            alert("Error " + result);
        } else {
            window.location.href = '/tiendas?mensaje=successAddTienda';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al crear la tienda.');
    }
}