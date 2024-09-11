document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('createUserForm').addEventListener('submit', handleSubmit);
    agregarTiendasALista();
});

async function agregarTiendasALista(){
    fetch('/api/tiendas')
    .then(response => response.json())
    .then(tiendas => {
        const seleccionTienda = document.querySelector('#idTienda');
        seleccionTienda.innerHTML = '';

        tiendas.forEach(tienda => {
            seleccionTienda.innerHTML += "<option value=" +tienda.idTienda+ ">" +tienda.idTienda+ "</option>"
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de tiendas:', error);
    });
}
async function handleSubmit(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    const data = new URLSearchParams(formData).toString();
    
    try {
        const response = await fetch('/crearUsuario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: data
        });

        const result = await response.text();
        
        if (response.status === 400) {
            if (result.includes('El nombre de usuario ya existe')) {
                alert("Ese nombre de usuario ya existe.");
            } else if (result.includes('La tienda no existe')) {
                alert("Esa tienda no existe");
            }
        } else {
            window.location.href = '/usuarios?mensaje=successAddUser';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al crear el usuario.');
    }
}
