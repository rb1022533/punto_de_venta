document.addEventListener("DOMContentLoaded", function () {
    const input = document.getElementById("filtro-ventas");
    const tabla = document.getElementById("tabla-ventas");
    const filas = tabla.querySelectorAll("tbody tr"); // 🔹 solo filas del cuerpo de la tabla

    input.addEventListener("keyup", function () {
        const filtro = input.value.toLowerCase();

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
});