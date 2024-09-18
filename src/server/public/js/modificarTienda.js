document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const idTienda = params.get('idTienda');

    fetch(`/tienda/${idTienda}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('idTienda').value = data.idTienda;
            document.getElementById('direccion').value = data.direccion;
            document.getElementById('ciudad').value = data.ciudad;
            document.getElementById('provincia').value = data.provincia;
            document.getElementById('habilitado').value = data.habilitado.toString();
        })
        .catch(error => {
            console.error('Error al cargar los datos de la tienda:', error);
        });

    document.getElementById('editTiendaForm').addEventListener('submit', handleSubmit);
});

async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = new URLSearchParams(formData).toString();

    try {
        const response = await fetch('/modificarTienda', {
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
            window.location.href = '/tiendas?mensaje=successModifyTienda';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al modificar la tienda.');
    }
}

