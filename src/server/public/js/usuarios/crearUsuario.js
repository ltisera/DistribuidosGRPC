document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('createUserForm').addEventListener('submit', handleSubmit);
    document.getElementById('uploadCsvForm').addEventListener('submit', handleCsvUpload);
    agregarTiendasALista();
});

function cambioEnSelect(){
    var select = document.getElementById("casaCentral");
    var tienda = document.getElementById("idTienda")
    if (select.value == "true"){
        tienda.style.display = "none";
        tienda.value = "1";
    }else {
        tienda.value = tienda.options[1].value;
        tienda.style.display = "inline";    
    }
}

async function agregarTiendasALista(){
    fetch('/api/tiendas')
    .then(response => response.json())
    .then(tiendas => {
        const seleccionTienda = document.querySelector('#idTienda');
        seleccionTienda.innerHTML = '';

        tiendas.forEach(tienda => {
            if(tienda.idTienda == 1){
                seleccionTienda.innerHTML += "<option hidden value=" +tienda.idTienda+ ">" +tienda.idTienda+ "</option>"
            }else {
                seleccionTienda.innerHTML += "<option value=" +tienda.idTienda+ ">" +tienda.idTienda+ "</option>"
            }
        });
        cambioEnSelect();
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

// Función para manejar la carga del archivo CSV
async function handleCsvUpload(event) {
    event.preventDefault();

    const csvFile = document.getElementById('csvFile').files[0];
    if (!csvFile) {
        alert('Por favor seleccione un archivo CSV.');
        return;
    }

    const formData = new FormData();
    formData.append('csvFile', csvFile);

    try {
        const response = await fetch('/cargarCSV', {
            method: 'POST',
            body: formData
        });

        if (response.status === 400) {
            const result = await response.json(); // Cambiar a JSON para manejar errores
            // Concatenar errores en un string
            const errorMessages = result.errores.join('\n'); // Usar salto de línea para separar errores
            alert(`Errores:\n${errorMessages}`); // Mostrar todos los errores en una sola alerta
        } else {
            alert('Usuarios cargados exitosamente.');
            window.location.reload();
        }
    } catch (error) {
        console.error('Error al cargar el archivo CSV:', error);
        alert('Hubo un problema al cargar el archivo CSV.');
    }
}

