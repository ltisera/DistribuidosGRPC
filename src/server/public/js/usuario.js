document.addEventListener('DOMContentLoaded', () => {
    fetchUsuarios();
    document.querySelector('#filter-form').addEventListener('submit', (event) => {
        event.preventDefault();
        fetchUsuarios();
    });

    const params = new URLSearchParams(window.location.search);
    const mensaje = params.get('mensaje');

    if (mensaje) {
        let messageText = '';
        switch (mensaje) {
            case 'successAddUser':
                messageText = 'Usuario agregado con éxito!';
                break;
            case 'successModifyUser':
                messageText = 'Usuario actualizado con éxito!';
                break;
            case 'successDeleteUser':
                messageText = 'Usuario eliminado con éxito!';
                break;
            default:
                messageText = '';
        }

        if (messageText) {
            console.log("ShowPopUp")
            showPopup(messageText);
        }
    }
});

function showPopup(message) {
    const popup = document.getElementById('popup');
    if (popup) {
        popup.textContent = message;
        popup.classList.add('show');
        setTimeout(() => {
            popup.classList.remove('show');
        }, 3000);
    }
}

function modifyUser(idUsuario) {
    window.location.href = `/modificarUsuario?idUsuario=${idUsuario}`;
}

function deleteUser(idUsuario) {
    fetch('/eliminarUsuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ userId: idUsuario })
    })
    .then(response => {
        if (response.ok) {
            window.location.href = '/usuarios?mensaje=successDeleteUser';
        } else {
            console.error('Error al eliminar usuario');
        }
    })
    .catch(error => {
        console.error('Error al enviar solicitud de eliminación:', error);
    });
}

function fetchUsuarios() {
    const nombre = encodeURIComponent(document.querySelector('#nombre-filter').value);
    const idTienda = encodeURIComponent(document.querySelector('#tienda-filter').value);
    var urlFiltro = ""
    if(nombre || idTienda){
        urlFiltro =`/api/usuarios/filtrados?nombre=${nombre}&idTienda=${idTienda}`
    } else {
        urlFiltro ='/api/usuarios'
    }
    fetch(urlFiltro)
    .then(response => response.json())
    .then(users => {
        const tableBody = document.querySelector('#users-table tbody');
        tableBody.innerHTML = '';

        users.forEach(user => {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${user.idUsuario}</td>
                <td>${user.usuario}</td>
                <td>${user.habilitado ? 'Sí' : 'No'}</td>
                <td>${user.tienda}</td>
                <td>
                    <button class="btn-modify" onclick="modifyUser('${user.idUsuario}')">Modificar</button>
                    <button class="btn-delete" onclick="deleteUser('${user.idUsuario}')">Eliminar</button>
                </td>
            `;

            tableBody.appendChild(row);
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de usuarios:', error);
    });
}