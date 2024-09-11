document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('createUserForm').addEventListener('submit', handleSubmit);
});

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
