document.addEventListener("DOMContentLoaded", function () {
    const mensajesDiv = document.getElementById("django-messages");
    if (!mensajesDiv) return; // No hay mensajes

    const mensajesData = mensajesDiv.dataset.messages;
    if (!mensajesData) return;

    try {
        const mensajes = JSON.parse(mensajesData);
        mensajes.forEach(msg => alert(msg));
    } catch (error) {
        console.error("Error parseando mensajes de Django:", error);
    }
});