document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.querySelector("#add-producto");
    const table = document.querySelector("#productos-table");
    const totalForms = document.querySelector("#id_detalleventa_set-TOTAL_FORMS");
    
    // Guardar la fila vacía como template
    const templateRow = table.querySelector(".producto-form").cloneNode(true);
    templateRow.querySelectorAll("input, select").forEach(input => input.value = "");

    addButton.addEventListener("click", function () {
        const currentForms = table.querySelectorAll(".producto-form").length;
        const newRow = templateRow.cloneNode(true);

        // Reindexar inputs/selects
        newRow.querySelectorAll("input, select").forEach(input => {
            input.name = input.name.replace(/\d+/, currentForms);
            input.id = input.id.replace(/\d+/, currentForms);
            if (input.tagName === "SELECT") input.selectedIndex = 0;
            else input.value = "";
        });

        // Agregar botón eliminar
        const td = document.createElement("td");
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "remove-producto";
        btn.textContent = "Eliminar";
        td.appendChild(btn);
        newRow.appendChild(td);

        table.appendChild(newRow);
        totalForms.value = currentForms + 1;

        // Evento eliminar
        btn.addEventListener("click", () => {
            newRow.remove();
            const forms = table.querySelectorAll(".producto-form");
            totalForms.value = forms.length;

            // Reindexar todos
            forms.forEach((row, index) => {
                row.querySelectorAll("input, select").forEach(input => {
                    input.name = input.name.replace(/\d+/, index);
                    input.id = input.id.replace(/\d+/, index);
                });
            });
        });
    });
});