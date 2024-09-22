document.addEventListener('DOMContentLoaded', () => {
    agregarTiendasALista();
    document.getElementById('editProductoForm').addEventListener('submit', handleSubmit);
});

function agregarDetalles(){
    const params = new URLSearchParams(window.location.search);
    const idProducto = params.get('idProducto');
    const talle = params.get('talle');
    fetch(`/producto/${idProducto}/${talle}`)
        .then(response => response.json())
        .then(data => {
            console.log(data.tiendas.tiendas);
            document.getElementById('idProducto').value = data.producto.idProducto;
            document.getElementById('codigo').value = data.producto.codigo;
            document.getElementById('nombre').value = data.producto.nombre;
            document.getElementById('foto').value = data.producto.foto;
            document.getElementById('color').value = data.producto.color;
            document.getElementById('talle').value = talle;
            document.getElementById('talleTexto').value = talle;
            data.tiendas.tiendas.forEach((tienda, index) => {
                if (tienda.idTienda != 1){
                    console.log(`#${tienda.idTienda}`);
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
        agregarDetalles();
    })
    .catch(error => {
        console.error('Error al cargar la lista de tiendas:', error);
    });
}

async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);


    const tiendas = [];
    document.querySelectorAll('#listaTiendas input[type="checkbox"]').forEach(checkbox => {
        tiendas.push({ id: checkbox.id, estado: checkbox.checked }); 
    });

    formData.append('tiendas', JSON.stringify(tiendas));

    const data = new URLSearchParams(formData).toString();

    try {
        const response = await fetch('/modificarProducto', {
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
            window.location.href = '/productos?mensaje=successModifyProducto';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al modificar la producto.');
    }
}

