document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar el enlace del símbolo © y agregar el evento click
    document.getElementById('logout-link').addEventListener('click', function(event) {
        event.preventDefault();  // Esto evita que la página se redirija a '#'
        limpiarCarritoAlDesloguear();  // Llama a la función para limpiar el carrito
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

// Función para limpiar el carrito del Local Storage
function limpiarCarritoAlDesloguear() {
    localStorage.removeItem('carrito');  // Elimina el carrito del Local Storage
    console.log('Carrito eliminado del caché');
}

let carrito = {};

function agregarAlCarrito(productoId) {
    if (carrito[productoId]) {
        carrito[productoId].cantidad += 1;
    } else {
        const nombre = document.querySelector(`[data-id="${productoId}"] .card-title`).textContent;
        const precio = parseInt(document.querySelector(`[data-id="${productoId}"] .price`).textContent.replace('$', ''), 10); // Convertimos a entero
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
    if (Object.keys(carrito).length > 0) {  // Solo mostrar el log si el carrito no está vacío
        console.log("Actualizando carrito, contenido actual:", carrito);
    }
    
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
                <span>$${(item.precio * item.cantidad).toLocaleString('es-CL')}</span>
                <button class="btn btn-sm btn-danger" onclick="eliminarDelCarrito(${id})">X</button>
            </div>
        `;
    }

    cartTotal.textContent = `$${total.toLocaleString('es-CL')}`;
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

// Función para enviar el pedido
function agregarPedido() {
    if (!carrito || Object.keys(carrito).length === 0) {
        alert("El carrito está vacío. Agrega productos antes de solicitar un pedido.");
        return;
    }

    const carritoItems = Object.keys(carrito).map(id => ({
        id: id,
        nombre: carrito[id].nombre,
        precio: carrito[id].precio,
        cantidad: carrito[id].cantidad
    }));

    console.log("Carrito a enviar:", carritoItems);

    fetch(agregarPedidoUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrfToken,
        },
        body: JSON.stringify({ carrito: carritoItems }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error en la solicitud: " + response.statusText);
        }
        return response.json();
    })
    .then(data => {
        console.log("Respuesta del servidor:", data);
        if (data.mensaje) {
            alert(data.mensaje);  // Muestra mensaje de éxito
            moverPedidoAlHistorial(carritoItems);  // Mover el pedido al historial
            carrito = {};  // Vaciar el carrito actual
            actualizarCarrito();  // Refrescar la vista del carrito
            guardarCarritoEnLocalStorage();
        } else if (data.error) {
            alert(data.error);
        }
    })
    .catch(error => {
        console.error('Error al procesar la solicitud:', error);
        alert('Hubo un problema al procesar el pedido. Inténtalo de nuevo más tarde.');
    });
}


// Función para mover el pedido actual al historial de pedidos
function moverPedidoAlHistorial(nuevoPedido) {
    console.log("Ejecutando moverPedidoAlHistorial con nuevo pedido:", nuevoPedido);
    const pedidosRealizadosDiv = document.getElementById("pedidos-realizados");

    // Crear una variable para almacenar el HTML de todos los productos
    let pedidoHtml = pedidosRealizadosDiv.innerHTML;
    let totalPedido = 0;

    // Crear HTML de los productos del nuevo pedido
    nuevoPedido.forEach(item => {
        totalPedido += item.precio * item.cantidad;
        pedidoHtml += `<span>${item.nombre} (${item.cantidad}) - $${(item.precio * item.cantidad).toLocaleString('es-CL')}</span><br>`;
    });

    // Actualizar el total acumulado en el historial
    let totalActual = parseFloat(pedidosRealizadosDiv.getAttribute('data-total') || '0');
    totalActual += totalPedido;
    pedidosRealizadosDiv.setAttribute('data-total', totalActual);

    // Mostrar el total acumulado solo una vez al final de todos los productos
    pedidoHtml += `<strong>Total acumulado: $${totalActual.toLocaleString('es-CL')}</strong><br>`;

    // Actualizar el contenido del historial en el DOM
    pedidosRealizadosDiv.innerHTML = pedidoHtml;

    // Guardar el historial en el Local Storage
    guardarHistorialEnLocalStorage(pedidoHtml, totalActual);

    console.log("Contenido actualizado de pedidos-realizados:", pedidosRealizadosDiv.innerHTML);
}

// Función para guardar el historial de pedidos en el Local Storage
function guardarHistorialEnLocalStorage(pedidoHtml, totalActual) {
    const historial = {
        contenido: pedidoHtml,
        total: totalActual
    };
    localStorage.setItem('historialPedidos', JSON.stringify(historial));
}

function cargarHistorialDesdeLocalStorage() {
    const historialGuardado = localStorage.getItem('historialPedidos');
    if (historialGuardado) {
        const historial = JSON.parse(historialGuardado);
        const pedidosRealizadosDiv = document.getElementById("pedidos-realizados");
        pedidosRealizadosDiv.innerHTML = historial.contenido;
        pedidosRealizadosDiv.setAttribute('data-total', historial.total);
    }
}

// Llama a esta función al cargar la página
document.addEventListener('DOMContentLoaded', function() {
    cargarHistorialDesdeLocalStorage();  // Cargar el historial guardado en el Local Storage
    cargarCarritoDesdeLocalStorage();    // Cargar el carrito desde el Local Storage
    actualizarCarrito();                 // Actualizar la vista del carrito
});

//Borra el localstorage
function borrarHistorial() {
    // Elimina el historial de pedidos del Local Storage
    localStorage.removeItem('historialPedidos');
    
    // Limpia el contenido de la sección "Pedidos realizados"
    const pedidosRealizadosDiv = document.getElementById("pedidos-realizados");
    pedidosRealizadosDiv.innerHTML = '<p>No hay pedidos realizados.</p>';
    pedidosRealizadosDiv.setAttribute('data-total', '0');

    console.log("Historial de pedidos eliminado del Local Storage y limpiado en el DOM.");
}
