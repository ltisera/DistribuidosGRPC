document.addEventListener('DOMContentLoaded', () => {
    fetchStock();
    document.querySelector('#filter-form').addEventListener('submit', (event) => {
        event.preventDefault();
        fetchStock();
    });

    const params = new URLSearchParams(window.location.search);
    const mensaje = params.get('mensaje');

    if (mensaje) {
        let messageText = '';
        switch (mensaje) {
            case 'successAddStock':
                messageText = 'Stock agregado con éxito!';
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

function fetchStock() {
    const codigo = encodeURIComponent(document.querySelector('#codigo-filter').value);
    const nombre = encodeURIComponent(document.querySelector('#nombre-filter').value);
    const talle = encodeURIComponent(document.querySelector('#talle-filter').value);
    const color = encodeURIComponent(document.querySelector('#color-filter').value);
    var urlFiltro = ""
    if(codigo || nombre || talle || color){
        urlFiltro = `/api/stock/filtrado?codigo=${codigo}&nombre=${nombre}&talle=${talle}&color=${color}`
    } else {
        urlFiltro = '/api/stock'
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
                <div class="box c2 ${bordeB} bordeR">${producto.idStock}</div>
                <div class="box c3 ${bordeB}">${producto.codigo}</div>
                <div class="box c4 ${bordeB}">${producto.nombre}</div>
                <div class="box c5 ${bordeB}">${producto.color}</div>
                <div class="box c6 ${bordeB} bordeR">${producto.talle} </div>
                <div class="box c6 ${bordeB}">${producto.cantidad}</div>             
                <div class="box c7 ${bordeB}">
                    <form id="agregarStockForm" action="/agregarStock" method="post">
                        <input type="hidden" id="idStock" name="idStock" value="${producto.idStock}">
                        <input type="number" id="cantidad" name="cantidad" required>
                        <button class = "buttonAdd" onclick="agregarStock()">+</button>
                    </form>
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

async function agregarStock(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = new URLSearchParams(formData).toString();

    console.log(data);
    
    try {
        const response = await fetch('/agregarStock', {
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
            window.location.href = '/stock?mensaje=successAddStock';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al agregar el stock del producto.');
    }
}