document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const idUsuario = params.get('idUsuario');
    agregarTiendasALista();

    fetch(`/usuario/${idUsuario}`)
        .then(response => response.json())
        .then(data => {
            document.getElementById('userId').value = data.idUsuario;
            document.getElementById('usuario').value = data.usuario;
            document.getElementById('password').value = data.password;
            document.getElementById('nombre').value = data.nombre;
            document.getElementById('apellido').value = data.apellido;
            document.getElementById('casaCentral').value = data.casaCentral.toString();
            const selectTienda = document.getElementById('idTienda');
            const opciones = selectTienda.options;
            for (let i = 0; i < opciones.length; i++) {
                if (opciones[i].value === data.idTienda.toString()) {
                    selectTienda.selectedIndex = i;
                    break;
                }
        }
        })
        .catch(error => {
            console.error('Error al cargar los datos del usuario:', error);
        });

    document.getElementById('editUserForm').addEventListener('submit', handleSubmit);
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
        const response = await fetch('/modificarUsuario', {
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
            window.location.href = '/usuarios?mensaje=successModifyUser';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Hubo un problema al modificar el usuario.');
    }
}

