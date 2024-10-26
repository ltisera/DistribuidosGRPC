document.addEventListener('DOMContentLoaded', () => {
    fetchNovedades();
    document.querySelector('#filter-form').addEventListener('submit', (event) => {
        event.preventDefault();
        fetchProductos();
    });

    const params = new URLSearchParams(window.location.search);
    const mensaje = params.get('mensaje');

    if (mensaje) {
        let messageText = '';
        switch (mensaje) {
            case 'successAddProducto':
                messageText = 'Producto agregado con éxito!';
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

function agregarNovedad(url, nombre, codigo, talle, color) {
    fetch('/agregarNovedad', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            url: url,
            nombre: nombre,
            codigo: codigo,
            talle: talle,
            color: color,
         })
    })
    .then(response => response.text())
    .then(result => {
        console.log("Resultado del agregado:", result);
        if (result === 'failureAddNovedad') {
            window.location.href = '/novedades?mensaje=failureAddNovedad';
        } else if (result === 'SuccessAddNovedad') {
            window.location.href = '/ordenes?mensaje=SuccessAddNovedad';
        } else {
            console.error('Respuesta inesperada:', result);
        }
        window.location.reload();
    })
    .catch(error => {
        console.error('Error al enviar solicitud de agregado:', error);
    });
}

function eliminarNovedad(codigo) {
    fetch('/eliminarNovedad', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ codigo: codigo })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/novedades?mensaje=successDeleteNovedad';
        } else {
            console.error('Error al eliminar novedad');
        }
    })
    .catch(error => {
        console.error('Error al enviar solicitud de eliminación:', error);
    });
}

function fetchNovedades() {
    url = '/api/novedades'
    fetch(url)
    .then(response => response.json())
    .then(novedades => {
        const divHtml = document.querySelector('#rellenarNovedades');
        divHtml.innerHTML = "";
        novedades.forEach((novedad, index) => {
            var bordeB = "";
            if(index === novedades.length - 1){
                bordeB = "bordeB"
            }
            var nuevaDiv = `
            <div class="container col${1 + (index % 2)}">
                <div class="box ${bordeB}">
                    <img class="box cajaFoto" src=${novedad.url}></img>
                </div>
                
                <div class="box c1 ${bordeB} bordeR">${novedad.codigo}</div>
                <div class="box c2 ${bordeB}">${novedad.nombre}</div>
                <div class="box c3 ${bordeB}">${novedad.talle}</div>
                <div class="box c4 ${bordeB}">${novedad.color}</div>            
                <div class="box c5 ${bordeB}">
                    <button class="btn-modify" onclick="agregarNovedad('${novedad.url}', '${novedad.nombre}', '${novedad.codigo}', '${novedad.talle}', '${novedad.color}')">Agregar</button>
                    <button class="btn-delete" onclick="eliminarNovedad('${novedad.codigo}')">Eliminar</button>
                </div>
            </div>
            `;
            divHtml.innerHTML += nuevaDiv;
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de novedades:', error);
    });
}