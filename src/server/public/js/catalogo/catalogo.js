let id_tienda_cache;

document.addEventListener('DOMContentLoaded', () => {
    traerCatalogos();
});

function traerCatalogos() {
    console.log("Entro a traer catalogos")
    obtenerIdTienda().then(idTienda => {
        console.log("Obtuvo idTienda")
        let xmlBody = 
        `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:8080/soap">
            <soap:Body>
                <tns:ConsultarCatalogos>
                    <tns:id_tienda>${idTienda}</tns:id_tienda>
                </tns:ConsultarCatalogos>
            </soap:Body>
        </soap:Envelope>`;

        fetch('http://localhost:8080/listaCatalogosSoap', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/xml'
            },
            body: xmlBody
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.text();
        })
        .then(resultados => {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(resultados, "text/xml");
            const catalogos = xmlDoc.getElementsByTagName("Catalogo");
            const divHtml = document.querySelector('#rellenarCatalogos');
            divHtml.innerHTML = "";
            console.log("Catalogos: ", catalogos)
            for (let catalogo of catalogos) {
                const idCatalogo = catalogo.getElementsByTagName("IdCatalogo")[0].textContent;
                const nombre = catalogo.getElementsByTagName("Nombre")[0].textContent;
                const idTienda = catalogo.getElementsByTagName("IdTienda")[0].textContent;
                const nuevaDiv = `
                    <div class="container col">
                        <div class="box c1">${idCatalogo}</div>
                        <div class="box c2">${nombre}</div>
                        <div class="box c3">${idTienda}</div>
                        <div class="box c4">
                            <button class="btn-modify" onclick="modifyCatalogo('${idCatalogo}')">Modificar</button>
                            <button class="btn-delete" onclick="deleteCatalogo('${idCatalogo}')">Eliminar</button>
                        </div>
                    </div>
                `;
        
                divHtml.innerHTML += nuevaDiv;
            }
        })
        .catch(error => {
            console.error('Error al traer catalogos:', error);
        });
    })
}

function deleteCatalogo(idCatalogo) {
    let xmlBody = 
    `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:8080/soap">
        <soap:Body>
            <tns:EliminarCatalogo>
                <tns:id_catalogo>${idCatalogo}</tns:id_catalogo>
            </tns:EliminarCatalogo>
        </soap:Body>
    </soap:Envelope>`;

    fetch('http://localhost:8080/eliminarCatalogoSoap', {
        method: 'POST',
        headers: {
            'Content-Type': 'text/xml'
        },
        body: xmlBody
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.text();
    })
    .then(result => {
        traerCatalogos();
    })
    .catch(error => {
        console.error('Error al eliminar catálogo:', error);
    });
}

function obtenerIdTienda() {
    console.log("Obteniendo idTienda")
    if (id_tienda_cache) {
        return Promise.resolve(id_tienda_cache);
    }
    
    return fetch('/obtenerTiendaActual')
        .then(response => {
            if (!response.ok) {
                throw new Error('No se pudo obtener la tienda actual');
            }
            return response.json();
        })
        .then(data => {
            id_tienda_cache = data;
            return id_tienda_cache;
        });
}
