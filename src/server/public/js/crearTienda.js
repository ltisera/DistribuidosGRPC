document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('createTiendaForm').addEventListener('submit', handleSubmit);
});

async function handleSubmit(event) {
    event.preventDefault();  // Evita el comportamiento predeterminado de enviar el formulario

    const formData = new FormData(event.target);  // Recoge los datos del formulario
    const data = new URLSearchParams(formData).toString();  // Convierte los datos a una cadena de URL

    try {
        // Envío de datos al servidor con fetch
        const response = await fetch('/crearTienda', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

        const result = await response.text();  // Leer la respuesta como texto
        
        // Manejo de la respuesta del servidor
        if (response.status === 400) {
            alert("Hubo un error al crear la tienda. Verifica los datos.");
        } else {
            // Redirigir a otra página si la tienda se creó correctamente
            window.location.href = '/tiendas?mensaje=successAddStore';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al crear la tienda.');
    }
}