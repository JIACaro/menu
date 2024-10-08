document.addEventListener('DOMContentLoaded', function() {
    // Seleccionar el enlace del símbolo © y agregar el evento click
    document.getElementById('logout-link').addEventListener('click', function(event) {
        event.preventDefault();  // Esto evita que la página se redirija a '#'
        document.getElementById('logout-form').submit();  // Enviar el formulario de logout
    });
});
