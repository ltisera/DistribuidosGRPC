document.addEventListener('DOMContentLoaded', () => {
    fetchOrdenes();

    const params = new URLSearchParams(window.location.search);
    const mensaje = params.get('mensaje');

    if (mensaje) {
        let messageText = '';
        let messageType = 'success';

        switch (mensaje) {
            case 'successAddOrden':
                messageText = 'Orden agregada con éxito!';
                break;
            case 'successModifyOrden':
                messageText = 'Orden actualizada con éxito!';
                break;
            case 'failureModifyOrden':
                messageText = 'El estado debe ser ACEPTADA';
                messageType = 'error';
                break;
            case 'successDeleteOrden':
                messageText = 'Orden eliminada con éxito!';
                break;
            default:
                messageText = '';
        }

        if (messageText) {
            console.log("ShowPopUp")
            showPopup(messageText, messageType);
        }
    }
});

function showPopup(message, type) {
    const popup = document.getElementById('popup');
    if (popup) {
        popup.textContent = message;
        popup.classList.remove('success', 'error');
        popup.classList.add(type === 'error' ? 'error' : 'success');
        popup.classList.add('show');
        setTimeout(() => {
            popup.classList.remove('show');
        }, 3000);
    }
}

function modifyOrden(idOrdenDeCompra) {
    fetch('/modificarOrden', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ordenId: idOrdenDeCompra })
    })
    .then(response => response.text())
    .then(result => {
        console.log("Resultado de la modificación:", result);
        if (result === 'failureModifyOrden') {
            window.location.href = '/ordenes?mensaje=failureModifyOrden';
        } else if (result === 'successModifyOrden') {
            window.location.href = '/ordenes?mensaje=successModifyOrden';
        } else {
            console.error('Respuesta inesperada:', result);
        }
    })
    .catch(error => {
        console.error('Error al enviar solicitud de modificación:', error);
    });
}

function deleteOrden(idOrdenDeCompra) {
    fetch('/eliminarOrden', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ ordenId: idOrdenDeCompra })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/ordenes?mensaje=successDeleteOrden';
        } else {
            console.error('Error al eliminar orden');
        }
    })
    .catch(error => {
        console.error('Error al enviar solicitud de eliminación:', error);
    });
}

function fetchOrdenes() {
    fetch('api/ordenes')
    .then(response => response.json())
    .then(ordenes => {
        ordenes.sort((a, b) => a.idOrdenDeCompra - b.idOrdenDeCompra);

        const divHtml = document.querySelector('#rellenarOrdenes');
        divHtml.innerHTML = "";

        ordenes.forEach((orden, index) => {
            var bordeB = "";
            if(index === ordenes.length - 1){
                bordeB = "bordeB"
            }

            const fechaSolicitud = formatTimestamp(orden.fechaSolicitud * 1);
            const fechaRecepcion = formatTimestamp(orden.fechaRecepcion * 1);

            var nuevaDiv = `
            <div class="container col${1 + (index % 2)}">
                <div class="box c1 ${bordeB} bordeR">${orden.idOrdenDeCompra}</div>
                <div class="box c2 ${bordeB}">${orden.idStock}</div>
                <div class="box c3 ${bordeB}">${orden.cantidad}</div>
                <div class="box c4 ${bordeB}">${orden.estado}</div>
                <div class="box c5 ${bordeB}"> ${orden.observaciones}</div>
                <div class="box c5 ${bordeB} bordeR">${fechaSolicitud}</div>
                <div class="box c5 ${bordeB}">${fechaRecepcion}</div>    
                <div class="box c6 ${bordeB}">${orden.ordenDeDespacho}</div>             
                <div class="box c7 ${bordeB}">
                    <button class="btn-modify" onclick="modifyOrden('${orden.idOrdenDeCompra}')">Recibir</button>
                    <button class="btn-delete" onclick="deleteOrden('${orden.idOrdenDeCompra}')">Eliminar</button>
                </div>
            </div>
            `;
            divHtml.innerHTML += nuevaDiv;
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de ordenes:', error);
    });
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    if (isNaN(date.getTime()) || date.getTime() == 0) {
        return 'Fecha inválida';
    }
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false };
    return date.toLocaleString('es-ES', options);
}
