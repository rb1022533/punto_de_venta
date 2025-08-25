document.addEventListener("DOMContentLoaded", function () {
    const checkboxes = document.querySelectorAll(".pedido-checkbox");
    const editarBtn = document.getElementById("editar-pedido-btn");
    const eliminarBtn = document.getElementById("eliminar-pedido-btn");
    const selectAll = document.getElementById("seleccionar-todos");

    let pedidoSeleccionadoId = null;

    function actualizarBotones() {
        const checked = Array.from(checkboxes).filter(c => c.checked);
        if (checked.length === 1) {
            pedidoSeleccionadoId = checked[0].dataset.pedidoId;
            editarBtn.disabled = false;
            eliminarBtn.disabled = false;
        } else if (checked.length > 1) {
            pedidoSeleccionadoId = null;
            editarBtn.disabled = true;
            eliminarBtn.disabled = false;
        } else {
            pedidoSeleccionadoId = null;
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
        if (pedidoSeleccionadoId) {
            window.location.href = `/editar_pedido/${pedidoSeleccionadoId}/`;
        }
    });

    // Botón Eliminar mediante POST
    eliminarBtn.addEventListener("click", function () {
        const checked = Array.from(checkboxes).filter(c => c.checked);
        if (checked.length === 0) return;

        if (!confirm("¿Estás seguro de eliminar los pedidos seleccionados?")) return;

        // Obtener token CSRF
        const csrfInput = document.querySelector('input[name="csrfmiddlewaretoken"]');
        if (!csrfInput) {
            alert("Error: no se encontró el CSRF token.");
            return;
        }

        // Crear formulario dinámico
        const form = document.createElement("form");
        form.method = "POST";
        form.action = "/eliminar_pedidos/";

        // Agregar CSRF
        const tokenInput = document.createElement("input");
        tokenInput.type = "hidden";
        tokenInput.name = "csrfmiddlewaretoken";
        tokenInput.value = csrfInput.value;
        form.appendChild(tokenInput);

        // Agregar IDs de pedidos
        checked.forEach(c => {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "pedidos_ids";
            input.value = c.dataset.pedidoId;
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
    // ========================
    // 🔍 Filtro de pedidos
    // ========================
    const inputFiltro = document.getElementById("filtro-pedidos");
    const tablaPedidos = document.getElementById("tabla-pedidos");
    if (inputFiltro && tablaPedidos) {
        const filas = tablaPedidos.querySelectorAll("tbody tr");
    
        inputFiltro.addEventListener("keyup", function () {
            const filtro = inputFiltro.value.toLowerCase();
    
            filas.forEach(fila => {
                const celdas = fila.getElementsByTagName("td");
                let coincide = false;
    
                for (let j = 0; j < celdas.length; j++) {
                    if (celdas[j].textContent.toLowerCase().includes(filtro)) {
                        coincide = true;
                        break;
                    }
                }
    
                fila.style.display = coincide ? "" : "none";
            });
        });
    }
});
