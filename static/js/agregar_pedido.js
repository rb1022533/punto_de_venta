document.addEventListener("DOMContentLoaded", function () {
    const productoSelect = document.getElementById("producto-input");
    const cantidadInput = document.getElementById("cantidad-input");
    const addBtn = document.getElementById("add-producto");
    const tableBody = document.querySelector("#productos-table tbody");
    const hiddenFields = document.getElementById("hidden-fields");

    function actualizarCamposOcultos() {
        hiddenFields.innerHTML = "";
        tableBody.querySelectorAll("tr").forEach(tr => {
            const pid = tr.dataset.productoId;
            const cant = tr.querySelector("td:nth-child(2)").textContent;

            const inputP = document.createElement("input");
            inputP.type = "hidden";
            inputP.name = "productos[]";
            inputP.value = pid;
            hiddenFields.appendChild(inputP);

            const inputC = document.createElement("input");
            inputC.type = "hidden";
            inputC.name = "cantidades[]";
            inputC.value = cant;
            hiddenFields.appendChild(inputC);
        });
    }

    addBtn.addEventListener("click", function () {
        const selectedOption = productoSelect.selectedOptions[0];
        const cantidad = parseInt(cantidadInput.value);

        if (!selectedOption || !cantidad || cantidad < 1) return alert("Selecciona producto y cantidad válida");

        const existing = tableBody.querySelector(`tr[data-producto-id='${selectedOption.value}']`);
        if (existing) return alert("El producto ya está agregado");

        const tr = document.createElement("tr");
        tr.dataset.productoId = selectedOption.value;
        const precio = parseFloat(selectedOption.dataset.precio);
        const subtotal = cantidad * precio;

        tr.innerHTML = `
            <td>${selectedOption.text}</td>
            <td>${cantidad}</td>
            <td>$${precio}</td>
            <td>$${subtotal}</td>
            <td><button type="button" class="eliminar-fila">Eliminar</button></td>
        `;
        tableBody.appendChild(tr);
        actualizarCamposOcultos();
    });

    // Eliminar fila
    tableBody.addEventListener("click", function (e) {
        if (e.target.classList.contains("eliminar-fila")) {
            e.target.closest("tr").remove();
            actualizarCamposOcultos();
        }
    });

    // Mensajes de Django (alert al guardar)
    const mensajesDiv = document.getElementById("django-messages");
    if (mensajesDiv) {
        const mensajes = JSON.parse(mensajesDiv.dataset.messages || "[]");
        mensajes.forEach(msg => alert(msg));
        mensajesDiv.remove(); // evitar que reaparezcan al recargar
    }

    // Inicializar Select2
    $('#producto-input').select2({ width: '300px' });
});