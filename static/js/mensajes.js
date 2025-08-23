document.addEventListener("DOMContentLoaded", function () {
    // Recorremos los mensajes que vienen como data-messages en el HTML
    const mensajesDiv = document.getElementById("django-messages");
    if (mensajesDiv) {
        const mensajes = mensajesDiv.dataset.messages;
        if (mensajes) {
            JSON.parse(mensajes).forEach(msg => alert(msg));
        }
    }
});

document.addEventListener("DOMContentLoaded", function() {
    const alertDivs = document.querySelectorAll(".alert");
    alertDivs.forEach(div => {
        alert(div.textContent.trim());
    });
});

document.addEventListener("DOMContentLoaded", function () {
    // Buscar el div que contiene los mensajes de Django
    const mensajesDiv = document.getElementById("django-messages");
    if (!mensajesDiv) return; // No hay mensajes

    // Obtener los mensajes desde el atributo data-messages
    const mensajesData = mensajesDiv.dataset.messages;
    if (!mensajesData) return;

    try {
        const mensajes = JSON.parse(mensajesData);
        mensajes.forEach(msg => alert(msg));
    } catch (error) {
        console.error("Error parseando mensajes de Django:", error);
    }
});