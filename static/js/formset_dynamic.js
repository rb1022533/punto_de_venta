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