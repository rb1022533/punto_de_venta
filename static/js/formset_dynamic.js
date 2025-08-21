document.addEventListener("DOMContentLoaded", function () {
    let addButton = document.getElementById("add-producto");
    let table = document.getElementById("productos-table");
    let totalForms = document.getElementById("id_detalleventa_set-TOTAL_FORMS");

    // Función para actualizar los botones eliminar
    function updateRemoveButtons() {
        document.querySelectorAll(".remove-producto").forEach(button => {
            button.onclick = function () {
                let row = this.closest("tr");
                row.remove();

                // Reindexar los nombres de los inputs
                document.querySelectorAll(".producto-form").forEach((row, index) => {
                    row.querySelectorAll("input, select").forEach(input => {
                        input.name = input.name.replace(/\d+/, index);
                        input.id = input.id.replace(/\d+/, index);
                    });
                });

                // Actualizar TOTAL_FORMS
                totalForms.value = document.querySelectorAll(".producto-form").length;
            };
        });
    }

    // Inicializar botones eliminar existentes
    updateRemoveButtons();

    // Agregar nueva fila
    addButton.addEventListener("click", function () {
        let currentForms = document.querySelectorAll(".producto-form").length;
        let newForm = document.querySelector(".producto-form").cloneNode(true);

        // Limpiar valores
        newForm.querySelectorAll("input, select").forEach(input => {
            if (input.tagName === "SELECT") input.selectedIndex = 0;
            else input.value = "";
        });

        // Reindexar nombres e IDs
        newForm.innerHTML = newForm.innerHTML.replace(/detalleventa_set-(\d+)-/g, `detalleventa_set-${currentForms}-`);

        // Agregar botón eliminar solo para nuevas filas
        let td = document.createElement("td");
        let btn = document.createElement("button");
        btn.type = "button";
        btn.className = "remove-producto";
        btn.textContent = "Eliminar";
        td.appendChild(btn);
        newForm.appendChild(td);

        table.appendChild(newForm);

        // Actualizar TOTAL_FORMS
        totalForms.value = currentForms + 1;

        // Reasignar eventos de eliminar
        updateRemoveButtons();
    });
});