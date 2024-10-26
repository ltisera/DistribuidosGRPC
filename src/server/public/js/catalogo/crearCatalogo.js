let id_tienda_cache;

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('createCatalogoForm').addEventListener('submit', (event) => {
        event.preventDefault();
        crearCatalogo();
    });
});

let enProceso = false;

function crearCatalogo() {
    if (enProceso) return;
    enProceso = true;
    obtenerIdTienda().then(idTienda => {
        const nombre = document.getElementById('nombre').value;

        let xmlBody = `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:8080/soap">
            <soap:Body>
                <tns:crear_catalogo>
                    <tns:nombre>${nombre}</tns:nombre>
                    <tns:id_tienda>${idTienda}</tns:id_tienda>
                </tns:crear_catalogo>
            </soap:Body>
        </soap:Envelope>`;

        console.log("XML", xmlBody)

        fetch('http://localhost:8080/soap/crear_catalogo', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/xml'
            },
            body: xmlBody
        })
        .then(response => {
            console.log("response", response)
            if (!response.ok) {
                throw new Error('Error al crear el catálogo');
            }
            return response.text();
        })
        .then(responseData => {
            console.log("Respuesta del servidor:", responseData);
            alert("Catálogo creado exitosamente");
        })
        .catch(error => {
            console.error('Error al crear catálogo:', error);
            alert('Hubo un problema al crear el catálogo.');
        })
        .finally(() => {
            enProceso = false;
            window.location.href = '/catalogos';
        });
    })
    .catch(error => {
        console.error('Error:', error);
        enProceso = false;
    });
}

function obtenerIdTienda() {
    console.log("Obteniendo idTienda")
    if (id_tienda_cache) {
        return Promise.resolve(id_tienda_cache);
    }
    
    return fetch('http://localhost:3000/obtenerTiendaActual')
        .then(response => {
            if (!response.ok) {
                throw new Error(`Error en la respuesta: ${response.status} ${response.statusText}`);
            }
            return response.json();
        })
        .then(data => {
            id_tienda_cache = data;
            return id_tienda_cache;
        });
}