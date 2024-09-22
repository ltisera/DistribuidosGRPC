document.addEventListener('DOMContentLoaded', () => {
    agregarTiendasALista();
    document.getElementById('addTalleForm').addEventListener('submit', handleSubmit);
});

function agregarDetalles(){
    const params = new URLSearchParams(window.location.search);
    const idProducto = params.get('idProducto');
    const talle = params.get('talle');

    fetch(`/producto/${idProducto}/${talle}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('idProducto').value = data.producto.idProducto;
            document.getElementById('codigo').value = data.producto.codigo;
            document.getElementById('nombre').value = data.producto.nombre;
            document.getElementById('color').value = data.producto.color;
            data.tiendas.tiendas.forEach((tienda, index) => {
                if (tienda.idTienda != 1){
                    document.getElementById(tienda.idTienda).checked = true;
                }
            });
        })
        .catch(error => {
            console.error('Error al cargar los datos de la producto:', error);
        });
}

function agregarTiendasALista(){
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
        agregarDetalles()
    })
    .catch(error => {
        console.error('Error al cargar la lista de tiendas:', error);
    });
}

async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);

    // Recoger los checkboxes seleccionados (tiendas)
    const tiendasSeleccionadas = [];
    document.querySelectorAll('#listaTiendas input[type="checkbox"]:checked').forEach(checkbox => {
        tiendasSeleccionadas.push(checkbox.id);
    });

    formData.append('tiendas', JSON.stringify(tiendasSeleccionadas));  // Añadir tiendas seleccionadas al formData

    const data = new URLSearchParams(formData).toString();

    try {
        const response = await fetch('/agregarTalle', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

        if (response.status === 400) {
            const errorText = await response.text();
            alert(errorText);
        } else {
            window.location.href = '/productos?mensaje=successAddTalle';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al agregar el talle.');
    }
}

