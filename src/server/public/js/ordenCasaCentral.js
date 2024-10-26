let id_usuario_cache;

document.addEventListener('DOMContentLoaded', () => {
    filtrarOrdenes();
    cargarFiltros();

    document.querySelector('#filter-form').addEventListener('submit', (event) => {
        event.preventDefault();
        filtrarOrdenes();
    });

    document.querySelector('#save-filter-form').addEventListener('submit', (event) => {
        event.preventDefault();
        guardarFiltro();
    });
});

function filtrarOrdenes() {
    const codigo_producto = document.getElementById('codigo_producto').value;
    const rango_fechas = [
        document.getElementById('fecha_inicio').value,
        document.getElementById('fecha_fin').value
    ];
    const estado = document.getElementById('estado').value;
    const id_tienda = document.getElementById('id_tienda').value;

    let xmlBody = `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:9000/soap">
        <soap:Body>
            <tns:ConsultarOrdenes>`;

    if (codigo_producto) {
        xmlBody += `<tns:codigo_producto>${codigo_producto}</tns:codigo_producto>`;
    }
    if (rango_fechas[0] && rango_fechas[1]) {
        xmlBody += `<tns:rango_fechas>${rango_fechas[0]},${rango_fechas[1]}</tns:rango_fechas>`;
    }
    if (estado) {
        xmlBody += `<tns:estado>${estado}</tns:estado>`;
    }
    if (id_tienda) {
        xmlBody += `<tns:id_tienda>${id_tienda}</tns:id_tienda>`;
    }

    xmlBody += `</tns:ConsultarOrdenes>
        </soap:Body>
    </soap:Envelope>`;

    fetch('http://localhost:9000/soap/consultar_ordenes', {
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
        const ordenes = xmlDoc.getElementsByTagName("Orden");
        const divHtml = document.querySelector('#rellenarOrdenes');
        divHtml.innerHTML = "";

        for (let orden of ordenes) {
            const idOrden = orden.getElementsByTagName("IdOrden")[0].textContent;
            const idStock = orden.getElementsByTagName("Producto")[0].textContent;
            const cantidad = orden.getElementsByTagName("CantidadTotal")[0].textContent;
            const estado = orden.getElementsByTagName("Estado")[0].textContent;
            const tienda = orden.getElementsByTagName("Tienda")[0].textContent;
    
            const nuevaDiv = `
                <div class="container col">
                    <div class="box c1">${idOrden}</div>
                    <div class="box c2">${idStock}</div>
                    <div class="box c3">${cantidad}</div>
                    <div class="box c4">${estado}</div>
                    <div class="box c5">${tienda}</div>
                </div>
            `;
    
            divHtml.innerHTML += nuevaDiv;
        }
    })
    .catch(error => {
        console.error('Error al filtrar órdenes:', error);
    });
}

let enProceso = false;

function guardarFiltro() {
    if (enProceso) return;
    enProceso = true;
    obtenerIdUsuario().then(id_usuario => {
        const nombre = document.getElementById('filtro_nombre').value;
        const codigo_producto = document.getElementById('codigo_producto').value;
        const rango_fechas = [
            document.getElementById('fecha_inicio').value,
            document.getElementById('fecha_fin').value
        ];
        const estado = document.getElementById('estado').value;
        const id_tienda = document.getElementById('id_tienda').value;

        let xmlBody = `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:9000/soap">
        <soap:Body>
            <tns:guardar_filtro>
            <tns:id_usuario>${id_usuario}</tns:id_usuario>
            <tns:nombre>${nombre}</tns:nombre>`;

        if (codigo_producto) {
            xmlBody += `<tns:codigo_producto>${codigo_producto}</tns:codigo_producto>`;
        }
        if (rango_fechas[0] && rango_fechas[1]) {
            xmlBody += `<tns:rango_fechas>${rango_fechas[0]},${rango_fechas[1]}</tns:rango_fechas>`;
        }
        if (estado) {
            xmlBody += `<tns:estado>${estado}</tns:estado>`;
        }
        if (id_tienda) {
            xmlBody += `<tns:id_tienda>${id_tienda}</tns:id_tienda>`;
        }

        xmlBody += `</tns:guardar_filtro>
            </soap:Body>
        </soap:Envelope>`;
     
        fetch('http://localhost:9000/soap/guardar_filtro', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/xml'
            },
            body: xmlBody
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al guardar el filtro');
            }
        })
        .catch(error => {
            console.error('Error al guardar filtro:', error);
        })
        .finally(() => {
            enProceso = false;
            location.reload();
        });
    });
}

function cargarFiltros() {
    obtenerIdUsuario().then(id_usuario => {
        let xmlBody = `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:9000/soap">
            <soap:Body>
                <tns:obtener_filtros>
                    <tns:id_usuario>${id_usuario}</tns:id_usuario>
                </tns:obtener_filtros>
            </soap:Body>
        </soap:Envelope>`;

        fetch('http://localhost:9000/soap/obtener_filtros', {
            method: 'POST',
            headers: {
                'Content-Type': 'text/xml'
            },
            body: xmlBody
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Error al obtener filtros');
            }
            return response.text();
        })
        .then(resultados => {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(resultados, "text/xml");
            const filtros = xmlDoc.getElementsByTagName("Filtro");
            const listaFiltros = document.getElementById('filtro_guardado');
            listaFiltros.innerHTML = '<option value="">--Seleccionar Filtro--</option>';

            for (let filtro of filtros) {
                const id = filtro.getElementsByTagName("Id")[0].textContent;
                const nombre = filtro.getElementsByTagName("Nombre")[0].textContent;
                
                const option = document.createElement('option');
                option.value = id;
                option.textContent = nombre;
                listaFiltros.appendChild(option);
            }
        })
        .catch(error => {
            console.error('Error al cargar filtros:', error);
        });
    });
}

function cargarFiltroSeleccionado() {
    const select = document.getElementById('filtro_guardado');
    const filtroId = select.value;

    const btnEditar = document.getElementById('btn-editar');
    const btnEliminar = document.getElementById('btn-eliminar');

    if (filtroId) {
        btnEditar.disabled = false;
        btnEliminar.disabled = false;
        fetch(`http://localhost:9000/soap/obtener_filtro?id=${filtroId}`)
            .then(response => response.text())
            .then(resultados => {
                const parser = new DOMParser();
                const xmlDoc = parser.parseFromString(resultados, "text/xml");

                const getValue = (tagName) => {
                    const element = xmlDoc.getElementsByTagName(tagName)[0];
                    return element ? element.textContent : '';
                };

                document.getElementById('codigo_producto').value = getValue("Producto");
                document.getElementById('fecha_inicio').value = getValue("RangoFechasStart");
                document.getElementById('fecha_fin').value = getValue("RangoFechasEnd");
                document.getElementById('estado').value = getValue("Estado");
                document.getElementById('id_tienda').value = getValue("IdTienda");
            })
            .catch(error => {
                console.error('Error al cargar el filtro seleccionado:', error);
            });
    } else {
        document.getElementById('codigo_producto').value = '';
        document.getElementById('fecha_inicio').value = '';
        document.getElementById('fecha_fin').value = '';
        document.getElementById('estado').value = '';
        document.getElementById('id_tienda').value = '';
        btnEditar.disabled = true;
        btnEliminar.disabled = true;
    }
}

function abrirModalEditar() {
    const select = document.getElementById('filtro_guardado');
    const filtroId = select.value;

    fetch(`http://localhost:9000/soap/obtener_filtro?id=${filtroId}`)
        .then(response => response.text())
        .then(result => {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(result, "text/xml");

            document.getElementById('editar_filtro_nombre').value = xmlDoc.getElementsByTagName("Nombre")[0].textContent;
            document.getElementById('editar_codigo_producto').value = xmlDoc.getElementsByTagName("Producto")[0].textContent;
            document.getElementById('editar_fecha_inicio').value = xmlDoc.getElementsByTagName("RangoFechasStart")[0].textContent;
            document.getElementById('editar_fecha_fin').value = xmlDoc.getElementsByTagName("RangoFechasEnd")[0].textContent;
            document.getElementById('editar_estado').value = xmlDoc.getElementsByTagName("Estado")[0].textContent;
            document.getElementById('editar_id_tienda').value = xmlDoc.getElementsByTagName("IdTienda")[0].textContent;

            document.getElementById('modal-editar').style.display = 'block';
        })
        .catch(error => {
            console.error('Error al cargar el filtro:', error);
        });
}

function cerrarModal() {
    document.getElementById('modal-editar').style.display = 'none';
}

function editarFiltro() {
    const filtroData = {
        id: document.getElementById('filtro_guardado').value,
        nombre: document.getElementById('editar_filtro_nombre').value,
        producto: document.getElementById('editar_codigo_producto').value,
        rangoFechasStart: document.getElementById('editar_fecha_inicio').value,
        rangoFechasEnd: document.getElementById('editar_fecha_fin').value,
        estado: document.getElementById('editar_estado').value,
        idTienda: document.getElementById('editar_id_tienda').value
    };

    let xmlBody = `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:9000/soap">
        <soap:Body>
            <tns:editar_filtro>
                <tns:id>${filtroData.id}</tns:id>
                <tns:nombre>${filtroData.nombre}</tns:nombre>
                <tns:codigo_producto>${filtroData.producto}</tns:codigo_producto>
                <tns:rango_fechas>${filtroData.rangoFechasStart},${filtroData.rangoFechasEnd}</tns:rango_fechas>
                <tns:estado>${filtroData.estado}</tns:estado>
                <tns:id_tienda>${filtroData.idTienda}</tns:id_tienda>
            </tns:editar_filtro>
        </soap:Body>
    </soap:Envelope>`;

    fetch(`http://localhost:9000/soap/editar_filtro`, {
        method: 'POST',
        headers: {
            'Content-Type': 'text/xml'
        },
        body: xmlBody
    })
    .then(response => response.text())
    .then(result => {
        console.log("Filtro editado:", result);
        cerrarModal();
    })
    .catch(error => {
        console.error('Error al editar el filtro:', error);
    })
    .finally(() => {
        location.reload();
    });
}

function eliminarFiltro() {
    const select = document.getElementById('filtro_guardado');
    const filtroId = select.value;

    if (!filtroId) {
        alert("Por favor, selecciona un filtro para eliminar.");
        return;
    }

    const xmlBody = `<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="http://localhost:9000/soap">
        <soap:Body>
            <tns:borrar_filtro>
                <tns:id>${filtroId}</tns:id>
            </tns:borrar_filtro>
        </soap:Body>
    </soap:Envelope>`;

    fetch(`http://localhost:9000/soap/borrar_filtro`, {
        method: 'POST',
        headers: {
            'Content-Type': 'text/xml'
        },
        body: xmlBody
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error al eliminar el filtro");
        }
        return response.text();
    })
    .then(result => {
        console.log("Filtro eliminado:", result);
        cargarFiltros();
    })
    .catch(error => {
        console.error('Error al eliminar el filtro:', error);
        alert('No se pudo eliminar el filtro. Intenta nuevamente.');
    })
    .finally(() => {
        location.reload();
    });
}

function formatTimestamp(timestamp) {
    const date = new Date(timestamp);
    if (isNaN(date.getTime()) || date.getTime() == 0) {
        return 'Fecha inválida';
    }
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false };
    return date.toLocaleString('es-ES', options);
}

function obtenerIdUsuario() {
    if (id_usuario_cache) {
        return Promise.resolve(id_usuario_cache);
    }
    
    console.log("Obteniendo usuario..");
    return fetch('/obtenerUsuarioActual')
        .then(response => {
            if (!response.ok) {
                throw new Error('No se pudo obtener el usuario actual');
            }
            return response.json();
        })
        .then(data => {
            console.log("Respuesta JSON: ", data);
            id_usuario_cache = data;
            return id_usuario_cache;
        });
}

