document.addEventListener('DOMContentLoaded', function() {
    function updateClock() {
        const clockElement = document.getElementById('clock');
        if (clockElement) {
            const now = new Date();
            const hours = now.getHours().toString().padStart(2, '0');
            const minutes = now.getMinutes().toString().padStart(2, '0');
            const period = hours >= 12 ? 'P.M' : 'A.M';
            clockElement.textContent = `${hours}:${minutes} ${period}`;
        }
    }
    setInterval(updateClock, 1000);
    updateClock();

    document.querySelectorAll('.check-button').forEach(button => {
        button.addEventListener('click', function() {
            const orderId = this.getAttribute('data-order-id'); 
            console.log("Order ID:", orderId);
            console.log("CSRF Token:", getCSRFToken());

            fetch(`http://127.0.0.1:8000/cocina/cambiar-estado-pedido/${orderId}/`, {

                method: 'POST',
                headers: {
                    'X-CSRFToken': getCSRFToken(),
                    'Content-Type': 'application/json',
                }
            })
            .then(response => {
                // Verifica si la respuesta es HTML en lugar de JSON
                if (response.headers.get("content-type") && response.headers.get("content-type").includes("text/html")) {
                    return response.text().then(html => {
                        console.error("Unexpected HTML response:", html);
                        throw new Error("Received HTML instead of JSON.");
                    });
                }
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    const orderCard = document.getElementById('order-card-' + orderId);
                    if (orderCard) {
                        orderCard.style.transition = "opacity 0.5s";
                        orderCard.style.opacity = 0;
                        setTimeout(() => {
                            orderCard.remove();
                        }, 500);
                    }
                } else {
                    console.error('Error:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

function getCSRFToken() {
    const token = document.cookie.split(';').find(row => row.trim().startsWith('csrftoken='));
    return token ? token.split('=')[1] : null;
}
