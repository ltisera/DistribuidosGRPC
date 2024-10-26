document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('createOrdenForm').addEventListener('submit', handleSubmit);
    agregarProductosALista();
});

async function agregarProductosALista(){
    fetch('/api/stock')
    .then(response => response.json())
    .then(productos => {
        const seleccionProducto = document.querySelector('#idStock');
        seleccionProducto.innerHTML = '';

        productos.forEach(producto => {
            if(producto.idStock == 1){
                seleccionProducto.innerHTML += "<option hidden value=" +producto.idStock+ ">" +producto.idStock+ "</option>"
            }else {
                seleccionProducto.innerHTML += "<option value=" +producto.idStock+ ">" +producto.idStock+ "</option>"
            }
        });
    })
    .catch(error => {
        console.error('Error al cargar la lista de productos:', error);
    });
}