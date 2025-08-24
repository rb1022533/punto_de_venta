document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll(".producto-checkbox");
    const editarBtn = document.getElementById("editar-producto-btn");
    const eliminarBtn = document.getElementById("eliminar-producto-btn");
    const selectAll = document.getElementById("seleccionar-todos");

    let productoSeleccionadoId = null;

    function actualizarBotones() {
        const checked = Array.from(checkboxes).filter(c => c.checked);
        if (checked.length === 1) {
            productoSeleccionadoId = checked[0].dataset.productoId;
            editarBtn.disabled = false;
            eliminarBtn.disabled = false;
        } else if (checked.length > 1) {
            productoSeleccionadoId = null;
            editarBtn.disabled = true;
            eliminarBtn.disabled = false;
        } else {
            productoSeleccionadoId = null;
            editarBtn.disabled = true;
            eliminarBtn.disabled = true;
        }

        if (selectAll) {
            selectAll.checked = checkboxes.length > 0 && Array.from(checkboxes).every(cb => cb.checked);
        }
    }

    checkboxes.forEach(cb => cb.addEventListener("change", actualizarBotones));

    // Botón Editar
    editarBtn.addEventListener("click", function () {
        if (productoSeleccionadoId) {
            window.location.href = `/editar_producto/${productoSeleccionadoId}/`;
        }
    });

    // Botón Eliminar (igual que en pedidos, con formulario dinámico)
    eliminarBtn.addEventListener("click", function () {
        const checked = Array.from(checkboxes).filter(c => c.checked);
        if (checked.length === 0) return;

        if (!confirm("¿Estás seguro de eliminar los productos seleccionados?")) return;

        // Obtener token CSRF
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (!csrfInput) {
            alert("Error: no se encontró el CSRF token.");
            return;
        }

        // Crear formulario dinámico
        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/eliminar_productos/";

        // Agregar CSRF
        const tokenInput = document.createElement("input");
        tokenInput.type = "hidden";
        tokenInput.name = "csrfmiddlewaretoken";
        tokenInput.value = csrfInput.value;
        form.appendChild(tokenInput);

        // Agregar IDs de productos
        checked.forEach(c => {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "productos_ids[]";  // importante: coincida con views
            input.value = c.dataset.productoId;
            form.appendChild(input);
        });

        document.body.appendChild(form);
        form.submit();
    });

    if (selectAll) {
        selectAll.addEventListener("change", function () {
            const checked = this.checked;
            checkboxes.forEach(cb => cb.checked = checked);
            actualizarBotones();
        });
    }

    actualizarBotones(); // inicializar
});