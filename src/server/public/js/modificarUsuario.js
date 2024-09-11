document.addEventListener('DOMContentLoaded', () => {
    const params = new URLSearchParams(window.location.search);
    const idUsuario = params.get('idUsuario');

    if (usuario) {
        fetch(`/usuario/${idUsuario}`)
            .then(response => response.json())
            .then(data => {
                document.getElementById('userId').value = data.idUsuario;
                document.getElementById('usuario').value = data.usuario;
                document.getElementById('password').value = data.password;
                document.getElementById('nombre').value = data.nombre;
                document.getElementById('apellido').value = data.apellido;
                document.getElementById('habilitado').value = data.habilitado.toString();
                document.getElementById('casaCentral').value = data.casaCentral.toString();
                document.getElementById('idTienda').value = data.idTienda;
            })
            .catch(error => {
                console.error('Error al cargar los datos del usuario:', error);
            });
    }

    document.getElementById('editUserForm').addEventListener('submit', handleSubmit);
});

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

