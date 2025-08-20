document.addEventListener("DOMContentLoaded", function () {
    let addButton = document.getElementById("add-producto");
    let table = document.getElementById("productos-table");
    let totalForms = document.getElementById("id_detalleventa_set-TOTAL_FORMS");

    addButton.addEventListener("click", function () {
        let currentForms = document.querySelectorAll(".producto-form").length;
        let newForm = document.querySelector(".producto-form").cloneNode(true);

        // Cambiar los nombres e IDs de los inputs
        newForm.innerHTML = newForm.innerHTML.replace(
            new RegExp(`detalleventa_set-(\\d+)-`, "g"),
            `detalleventa_set-${currentForms}-`
        );

        table.appendChild(newForm);
        totalForms.value = currentForms + 1; // actualizar TOTAL_FORMS
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form'); // el formulario de venta

    form.addEventListener('submit', function(e) {
        let error = false;

        document.querySelectorAll('.formset-row').forEach(row => {
            const select = row.querySelector('select'); // select de producto
            const cantidad = row.querySelector('input[name$="cantidad"]'); // input de cantidad

            if (select && cantidad) {
                const stock = parseInt(select.selectedOptions[0].dataset.stock);
                const qty = parseInt(cantidad.value);

                if (qty > stock) {
                    error = true;
                    alert(`No hay suficiente stock de ${select.selectedOptions[0].text}.\nStock disponible: ${stock}`);
                }
            }
        });

        if (error) e.preventDefault(); // detener envío si hay error
    });
});