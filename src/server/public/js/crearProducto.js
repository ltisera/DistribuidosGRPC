document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('createProductoForm').addEventListener('submit', handleSubmit);
    agregarTiendasALista();
});

async function agregarTiendasALista(){
    fetch('/api/tiendas')
    .then(response => response.json())
    .then(tiendas => {
        const listaTienda = document.querySelector('#listaTiendas');
        listaTienda.innerHTML = ``

        tiendas.forEach(tienda => {
            listaTienda.innerHTML += `
            <div class="tienda">
                <span class="textoTienda">${tienda.idTienda}&nbsp;${tienda.direccion}</span>
                <input type="checkbox" id="${tienda.idTienda}" name="${tienda.idTienda}">
            </div>
        `});
    })
    .catch(error => {
        console.error('Error al cargar la lista de tiendas:', error);
    });
}

async function handleSubmit(event) {
    event.preventDefault();  // Evita el comportamiento predeterminado de enviar el formulario

    const formData = new FormData(event.target);  // Recoge los datos del formulario
    const data = new URLSearchParams(formData).toString();  // Convierte los datos a una cadena de URL

    try {
        // Envío de datos al servidor con fetch
        const response = await fetch('/crearProducto', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

        const result = await response.text();  // Leer la respuesta como texto
        
        // Manejo de la respuesta del servidor
        if (response.status === 400) {
            alert(result);
        } else {
            // Redirigir a otra página si el producto se creó correctamente
            window.location.href = '/productos?mensaje=successAddProducto';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al crear el producto.');
    }
}