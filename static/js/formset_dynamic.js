document.addEventListener("DOMContentLoaded", function () {
    const addButtons = document.querySelectorAll("[id^='add-producto']");
    
    addButtons.forEach(addButton => {
        const table = addButton.closest("form").querySelector("#productos-table");
        const totalForms = table.closest("form").querySelector("input[id$='TOTAL_FORMS']");
        const prefix = totalForms.id.replace("-TOTAL_FORMS", "");

        // Función para actualizar botones eliminar
        function updateRemoveButtons() {
            table.querySelectorAll(".remove-producto").forEach(button => {
                button.onclick = function () {
                    const row = this.closest("tr");
                    row.remove();

                    // Reindexar inputs/selects
                    table.querySelectorAll(".producto-form").forEach((row, index) => {
                        row.querySelectorAll("input, select").forEach(input => {
                            input.name = input.name.replace(new RegExp(`${prefix}-(\\d+)-`), `${prefix}-${index}-`);
                            input.id = input.id.replace(new RegExp(`${prefix}-(\\d+)-`), `${prefix}-${index}-`);
                        });
                    });

                    // Actualizar TOTAL_FORMS
                    totalForms.value = table.querySelectorAll(".producto-form").length;
                };
            });
        }

        // Inicializar botones existentes
        updateRemoveButtons();

        // Agregar nueva fila
        addButton.addEventListener("click", function () {
            const currentForms = table.querySelectorAll(".producto-form").length;
            const newForm = table.querySelector(".producto-form").cloneNode(true);

            // Limpiar valores
            newForm.querySelectorAll("input, select").forEach(input => {
                if (input.tagName === "SELECT") input.selectedIndex = 0;
                else input.value = "";
            });

            // Reindexar nombres e IDs
            newForm.innerHTML = newForm.innerHTML.replace(
                new RegExp(`${prefix}-(\\d+)-`, "g"),
                `${prefix}-${currentForms}-`
            );

            // Agregar botón eliminar solo para nuevas filas
            const td = document.createElement("td");
            const btn = document.createElement("button");
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
});