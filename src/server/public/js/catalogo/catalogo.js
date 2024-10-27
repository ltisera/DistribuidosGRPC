let id_tienda_cache;
let id_catalogo;

document.addEventListener('DOMContentLoaded', () => {
    traerCatalogos();

    document.getElementById('btnGuardar').addEventListener('click', function() {
        const selectedProducts = Array.from(document.querySelectorAll('#listaProductos input[type="checkbox"]:checked'))
            .map(checkbox => {
                const productoDiv = checkbox.parentElement;
                const talle = productoDiv.querySelector('.talle-class').textContent;
                return `${checkbox.value},${talle}`;
            });
    
        const allProducts = Array.from(document.querySelectorAll('#listaProductos input[type="checkbox"]'));
        const unselectedProducts = allProducts.filter(checkbox => !checkbox.checked)
            .map(checkbox => {
                const productoDiv = checkbox.parentElement;
                const talle = productoDiv.querySelector('.talle-class').textContent;
                return `${checkbox.value},${talle}`;
            });
    
        console.log("Productos seleccionados: ", selectedProducts);
        console.log("Productos no seleccionados: ", unselectedProducts);
    
        agregarProductosAlCatalogo(id_catalogo, selectedProducts);
    
        if (unselectedProducts.length > 0) {
            eliminarProductosDelCatalogo(id_catalogo, unselectedProducts);
        }
    
        cerrarModal();
    });
});

function traerCatalogos() {
    obtenerIdTienda().then(idTienda => {
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
                            <button class="btn-export" onclick="exportarCatalogo('${idCatalogo}')">Exportar</button>
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

function modifyCatalogo(idCatalogo) {
    document.getElementById('modalModificar').style.display = 'block';
    id_catalogo = idCatalogo
    cargarProductosPorCatalogo(idCatalogo);
}

function cerrarModal() {
    document.getElementById('modalModificar').style.display = 'none';
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

function cargarProductosPorCatalogo(idCatalogo) {
    obtenerIdTienda().then(idTienda => {
        let xmlBody = 
        `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:8080/soap">
            <soap:Body>
                <tns:ConsultarProductos>
                    <tns:id_tienda>${idTienda}</tns:id_tienda>
                    <tns:id_catalogo>${idCatalogo}</tns:id_catalogo>
                </tns:ConsultarProductos>
            </soap:Body>
        </soap:Envelope>`;

        fetch('http://localhost:8080/listaProductosSoap', {
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
            const productos = xmlDoc.getElementsByTagName("Producto");
            const divHtml = document.querySelector('#listaProductos');
            divHtml.innerHTML = "";

            for (let producto of productos) {
                const idProducto = producto.getElementsByTagName("IdProducto")[0].textContent;
                const nombre = producto.getElementsByTagName("Nombre")[0].textContent;
                const foto = producto.getElementsByTagName("Foto")[0].textContent;
                const color = producto.getElementsByTagName("Color")[0].textContent;
                const talle = producto.getElementsByTagName("Talle")[0].textContent;
                const enCatalogo = producto.getElementsByTagName("EnCatalogo")[0].textContent === "true";

                const nuevaDiv = `
                    <div class="producto-item">
                        <input type="checkbox" id="producto_${idProducto}" value="${idProducto}" ${enCatalogo ? 'checked' : ''}>
                        <label for="producto_${idProducto}">
                            <img src="${foto}" alt="${nombre}" class="producto-foto">
                            <div>
                                <strong>${nombre}</strong><br>
                                Color: <span class="color-class">${color}</span>
                                Talle: <span class="talle-class">${talle}</span>
                            </div>
                        </label>
                    </div>
                `;
                divHtml.innerHTML += nuevaDiv;
            }
        })
        .catch(error => {
            console.error('Error al cargar productos:', error);
        });
    });
}

function agregarProductosAlCatalogo(idCatalogo, productos) {
    let xmlBody = 
    `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:8080/soap">
        <soap:Body>
            <tns:AgregarProductos>
                <tns:id_catalogo>${idCatalogo}</tns:id_catalogo>
                <tns:productos>${productos.join(',')}</tns:productos>
            </tns:AgregarProductos>
        </soap:Body>
    </soap:Envelope>`;

    fetch('http://localhost:8080/agregarProductosSoap', {
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
        console.error('Error al agregar productos:', error);
    });
}

function eliminarProductosDelCatalogo(idCatalogo, productos) {
    let xmlBody = 
    `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:8080/soap">
        <soap:Body>
            <tns:EliminarProductos>
                <tns:id_catalogo>${idCatalogo}</tns:id_catalogo>
                <tns:productos>${productos.join(',')}</tns:productos>
            </tns:EliminarProductos>
        </soap:Body>
    </soap:Envelope>`;

    fetch('http://localhost:8080/eliminarProductosSoap', {
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
        console.log("Productos eliminados del catálogo con éxito.");
        traerCatalogos();
    })
    .catch(error => {
        console.error('Error al eliminar productos:', error);
    });
}

function exportarCatalogo(idCatalogo) {
    obtenerIdTienda().then(idTienda => {
        let xmlBody = 
        `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:8080/soap">
            <soap:Body>
                <tns:ExportarCatalogo>
                    <tns:id_catalogo>${idCatalogo}</tns:id_catalogo>
                </tns:ExportarCatalogo>
            </soap:Body>
        </soap:Envelope>`;

        fetch('http://localhost:8080/exportarCatalogoSoap', {
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
            return response.blob(); // Esperamos un blob para el PDF
        })
        .then(pdfBlob => {
            // Crear un URL para el blob y descargar el PDF
            const url = URL.createObjectURL(pdfBlob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `catalogo_${idCatalogo}.pdf`; // Nombre del archivo
            document.body.appendChild(a);
            a.click();
            a.remove();
            URL.revokeObjectURL(url); // Liberar la URL del blob
        })
        .catch(error => {
            console.error('Error al exportar catálogo:', error);
        });
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
