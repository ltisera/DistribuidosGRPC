document.addEventListener('DOMContentLoaded', () => {
    fetchProductos();
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
            case 'successModifyProducto':
                messageText = 'Producto actualizado con éxito!';
                break;
            case 'successDeleteProducto':
                messageText = 'Producto eliminado con éxito!';
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

function modifyProducto(idProducto, talle) {
    window.location.href = `/modificarProducto?idProducto=${idProducto}&talle=${talle}`;
}

function deleteProducto(idProducto) {
    fetch('/eliminarProducto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ productoId: idProducto })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/productos?mensaje=successDeleteProducto';
        } else {
            console.error('Error al eliminar producto');
        }
    })
    .catch(error => {
        console.error('Error al enviar solicitud de eliminación:', error);
    });
}

function fetchProductos() {
    const codigo = encodeURIComponent(document.querySelector('#codigo-filter').value);
    const nombre = encodeURIComponent(document.querySelector('#nombre-filter').value);
    const talle = encodeURIComponent(document.querySelector('#talle-filter').value);
    const color = encodeURIComponent(document.querySelector('#color-filter').value);
    var urlFiltro = ""
    if(codigo || nombre || talle || color){
        console.log("entrea accccaaaaaaaaaa");
        urlFiltro = `/api/productos/filtrados?codigo=${codigo}&nombre=${nombre}&talle=${talle}&color=${color}`
    } else {
        urlFiltro = '/api/productos'
    } 
    fetch(urlFiltro)
    .then(response => response.json())
    .then(productos => {
        const divHtml = document.querySelector('#rellenarProductos');
        divHtml.innerHTML = "";
        productos.forEach((producto, index) => {
            var bordeB = "";
            if(index === productos.length - 1){
                bordeB = "bordeB"
            }
            var nuevaDiv = `
            <div class="container col${1 + (index % 2)}">
                <div class="box ${bordeB}">
                    <img class="box cajaFoto" src=${producto.foto}></img>
                </div>
                
                <div class="box c1 ${bordeB} bordeR">${producto.idProducto}</div>
                <div class="box c2 ${bordeB}">${producto.codigo}</div>
                <div class="box c3 ${bordeB}">${producto.nombre}</div>
                <div class="box c4 ${bordeB}">${producto.color}</div>
                <div class="box c5 ${bordeB} bordeR">${producto.talle} <button class = "buttonAdd">+</button></div>
                <div class="box c5 ${bordeB}">${producto.habilitado ? 'Sí' : 'No'}</div>             
                <div class="box c6 ${bordeB}">
                    <button class="btn-modify" onclick="modifyProducto('${producto.idProducto}','${producto.talle}')">Modificar</button>
                    <button class="btn-delete" onclick="deleteProducto('${producto.idProducto}')">Eliminar</button>
                </div>
            </div>
            `;
            divHtml.innerHTML += nuevaDiv;
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de productos:', error);
    });
}



async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = new URLSearchParams(formData).toString();
    
    try {
        const response = await fetch('/crearProducto', {
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
            window.location.href = '/productos?mensaje=successAddProducto';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al crear la producto.');
    }
}