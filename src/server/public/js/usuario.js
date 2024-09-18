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
        const divHtml = document.querySelector('#rellenarUsuarios');
        divHtml.innerHTML = "";;

        users.forEach((user, index) => {
            var bordeB = "";
            if(index === user.length - 1){
                bordeB = "bordeB"
            }
            var nuevaDiv = `
            <div class="container col${1 + (index % 2)}">
                <div class="box c1 ${bordeB} bordeR">${user.idUsuario}</div>
                <div class="box c2 ${bordeB}">${user.usuario}</div>
                <div class="box c3 ${bordeB}">${user.nombre}</div>
                <div class="box c4 ${bordeB}">${user.apellido}</div>
                <div class="box c5 ${bordeB}">${user.casaCentral ? 'Sí' : 'No'}</div>
                <div class="box c5 ${bordeB} bordeR">${user.tienda}</div>
                <div class="box c5 ${bordeB}">${user.habilitado ? 'Sí' : 'No'}</div>             
                <div class="box c6 ${bordeB}">
                    <button class="btn-modify" onclick="modifyUser('${user.idUsuario}')">Modificar</button>
                    <button class="btn-delete" onclick="deleteUser('${user.idUsuario}')">Eliminar</button>
                </div>
            </div>
            `;
            divHtml.innerHTML += nuevaDiv;
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de usuarios:', error);
    });
}