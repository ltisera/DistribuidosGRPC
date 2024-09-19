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

        tiendas.forEach((tienda, index) => {
            if (index > 0){
                listaTienda.innerHTML += `
                <div class="tienda col${1 + index%2}">
                    <div class="textoTienda">${tienda.idTienda} ${tienda.provincia}, ${tienda.ciudad}, ${tienda.direccion}</div>
                    <div>
                        <input type="checkbox" class="chckTienda" id="${tienda.idTienda}" name="${tienda.idTienda}">
                    </div>
                    
                </div>
            `}
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de tiendas:', error);
    });
}

async function handleSubmit(event) {
    event.preventDefault();  // Evita el comportamiento predeterminado de enviar el formulario

    const formData = new FormData(event.target);  // Recoge los datos del formulario

    // Recoger los checkboxes seleccionados (tiendas)
    const tiendasSeleccionadas = [];
    document.querySelectorAll('#listaTiendas input[type="checkbox"]:checked').forEach(checkbox => {
        tiendasSeleccionadas.push(checkbox.id);
    });

    formData.append('tiendasSeleccionadas', JSON.stringify(tiendasSeleccionadas));  // Añadir tiendas seleccionadas al formData

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