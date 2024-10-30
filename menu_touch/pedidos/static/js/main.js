document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar el enlace del símbolo © y agregar el evento click
    document.getElementById('logout-link').addEventListener('click', function(event) {
        event.preventDefault();  // Esto evita que la página se redirija a '#'
        document.getElementById('logout-form').submit();  // Enviar el formulario de logout
    });

    // Cargar el carrito desde el Local Storage al iniciar
    cargarCarritoDesdeLocalStorage();
    actualizarCarrito();

    // Evitar que el carrito se cierre al hacer clic en su interior
    const cartDropdown = document.getElementById('cartContent');
    cartDropdown.addEventListener('click', function(event) {
        event.stopPropagation();
    });
});

let carrito = {};

function agregarAlCarrito(productoId) {
    if (carrito[productoId]) {
        carrito[productoId].cantidad += 1;
    } else {
        const nombre = document.querySelector(`[data-id="${productoId}"] .card-title`).textContent;
        const precio = parseFloat(document.querySelector(`[data-id="${productoId}"] .price`).textContent.replace('$', ''));
        carrito[productoId] = { nombre, precio, cantidad: 1 };
    }
    actualizarCarrito();
    guardarCarritoEnLocalStorage();
}

function eliminarDelCarrito(productoId) {
    if (carrito[productoId]) {
        carrito[productoId].cantidad -= 1;
        if (carrito[productoId].cantidad === 0) {
            delete carrito[productoId];
        }
    }
    actualizarCarrito();
    guardarCarritoEnLocalStorage();
}

function actualizarCarrito() {
    const cartItems = document.getElementById("cart-items");
    const cartTotal = document.getElementById("cart-total");
    const cartCount = document.getElementById("cart-count");
    cartItems.innerHTML = '';
    let total = 0;
    let count = 0;

    for (const id in carrito) {
        const item = carrito[id];
        total += item.precio * item.cantidad;
        count += item.cantidad;

        cartItems.innerHTML += `
            <div class="d-flex justify-content-between align-items-center">
                <span>${item.nombre} (${item.cantidad})</span>
                <span>$${(item.precio * item.cantidad).toFixed(2)}</span>
                <button class="btn btn-sm btn-danger" onclick="eliminarDelCarrito(${id})">X</button>
            </div>
        `;
    }

    cartTotal.textContent = `$${total.toFixed(2)}`;
    cartCount.textContent = count;

    if (count === 0) {
        cartItems.innerHTML = '<p class="text-center">Tu carrito está vacío.</p>';
    }
}

// Función para guardar el carrito en el Local Storage
function guardarCarritoEnLocalStorage() {
    localStorage.setItem('carrito', JSON.stringify(carrito));
}

// Función para cargar el carrito desde el Local Storage
function cargarCarritoDesdeLocalStorage() {
    const carritoGuardado = localStorage.getItem('carrito');
    if (carritoGuardado) {
        carrito = JSON.parse(carritoGuardado);
    }
}
