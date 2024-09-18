document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const idProducto = params.get('idProducto');

    fetch(`/producto/${idProducto}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('idProducto').value = data.idProducto;
            document.getElementById('codigo').value = data.codigo;
            document.getElementById('nombre').value = data.nombre;
            document.getElementById('foto').value = data.foto;
            document.getElementById('color').value = data.color;
            document.getElementById('talle').value = data.talle;
        })
        .catch(error => {
            console.error('Error al cargar los datos de la producto:', error);
        });

    document.getElementById('editProductoForm').addEventListener('submit', handleSubmit);
});

async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
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

