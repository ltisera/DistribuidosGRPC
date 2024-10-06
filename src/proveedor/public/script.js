const addProductForm = document.getElementById('add-product-form');
const productList = document.getElementById('product-list');

window.onload = () => {
    fetchProducts();
    const firstTalleItem = document.querySelector('.talle-item');
    if (firstTalleItem) {
        addEventListenersToTalle(firstTalleItem);
    }
};

// TRAER TODOS LOS PRODUCTOS
function fetchProducts() {
    fetch('http://localhost:5000/api/productos')
        .then(response => response.json())
        .then(data => {
            productList.innerHTML = '';
            data.forEach(product => {
                const tr = document.createElement('tr');
                tr.innerHTML = `
                    <td><img src="${product.foto}" style="width:50px; height:50px;"></td>
                    <td>${product.nombre}</td>
                    <td>${product.color}</td>
                    <td>${product.talle}</td>
                    <td>${product.cantidad}</td>
                    <td>${product.idStock}</td>
                    <td>
                        <button onclick="openModal(${JSON.stringify(product).replace(/"/g, '&quot;')})">Modificar</button>
                    </td>
                `;
                productList.appendChild(tr);
            });
        })
        .catch(error => console.error('Error fetching products:', error));
}

// AGREGAR PRODUCTO
addProductForm.addEventListener('submit', (e) => {
    e.preventDefault();

    const nombre = document.getElementById('nombre').value;
    const foto = document.getElementById('foto').value;

    const talles = Array.from(document.querySelectorAll('.talle-item')).map(item => {
        const talle = item.querySelector('.talle').value;
        const colores = Array.from(item.querySelectorAll('.color-item')).map(colorItem => ({
            color: colorItem.querySelector('.color').value,
            cantidad: colorItem.querySelector('.cantidad').value
        }));
        return { talle, colores };
    });

    console.log(JSON.stringify({ nombre, foto, talles }));

    fetch('http://localhost:5000/api/producto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ nombre, foto, talles }),
    })
    .then(response => {
        if (response.ok) {
            fetchProducts();
            addProductForm.reset();
            location.reload();
        } else {
            console.error('Error adding product:', response);
        }
    })
    .catch(error => console.error('Error:', error));
});

// TALLES
document.getElementById('add-talle').addEventListener('click', () => {
    const talleContainer = document.getElementById('talle-container');
    const newTalleItem = document.createElement('div');
    newTalleItem.classList.add('talle-item');
    newTalleItem.innerHTML = `
        <input type="text" class="talle" placeholder="Talle" required>
        <div class="color-container">
            <div class="color-item">
                <input type="text" class="color" placeholder="Color" required>
                <input type="number" class="cantidad" placeholder="Cantidad" min="0" required>
                <button type="button" class="remove-color">Eliminar</button>
            </div>
        </div>
        <button type="button" class="add-color">Agregar Color</button>
        <button type="button" class="remove-talle">Eliminar Talle</button>
    `;
    talleContainer.appendChild(newTalleItem);

    addEventListenersToTalle(newTalleItem);
});

// AGREGAR EN CADA TALLE
function addEventListenersToTalle(talleItem) {
    talleItem.querySelector('.add-color').addEventListener('click', () => {
        const colorContainer = talleItem.querySelector('.color-container');
        const newColorItem = document.createElement('div');
        newColorItem.classList.add('color-item');
        newColorItem.innerHTML = `
            <input type="text" class="color" placeholder="Color" required>
            <input type="number" class="cantidad" placeholder="Cantidad" min="0" required>
            <button type="button" class="remove-color">Eliminar</button>
        `;
        colorContainer.appendChild(newColorItem);

        newColorItem.querySelector('.remove-color').addEventListener('click', () => {
            colorContainer.removeChild(newColorItem);
        });
    });
    
    talleItem.querySelector('.remove-talle').addEventListener('click', () => {
        talleItem.remove();
    });
}

// ABRIR MODAL CANTIDAD
function openModal(product) {
    document.getElementById('new-cantidad').value = product.cantidad;
    document.getElementById('stock-id').value = product.idStock;
    document.getElementById('modal').style.display = 'block';
}

// CERRAR MODAL CANTIDAD
function closeModal() {
    document.getElementById('modal').style.display = 'none';
}

// MODIFICAR CANTIDAD
document.getElementById('modify-product-form').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const idStock = document.getElementById('stock-id').value;
    const cantidad = document.getElementById('new-cantidad').value;

    fetch(`http://localhost:5000/api/producto/${idStock}/cantidad`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ cantidad }),
    })
    .then(response => {
        if (response.ok) {
            fetchProducts();
            closeModal();
        } else {
            console.error('Error modifying product:', response);
        }
    })
    .catch(error => console.error('Error:', error));
});