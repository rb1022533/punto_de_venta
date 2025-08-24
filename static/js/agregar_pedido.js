// static/js/agregar_pedido.js
$(document).ready(function() {
    $('#producto-input').select2({
        placeholder: "Selecciona un producto",
        allowClear: true
    });

    const cantidadInput = $('#cantidad-input');
    const addBtn = $('#add-producto');
    const tableBody = $('#productos-table tbody');
    const hiddenFields = $('#hidden-fields');

    addBtn.on('click', function() {
        const selectedOption = $('#producto-input option:selected');
        const productoId = selectedOption.val();
        const productoNombre = selectedOption.text();
        const precioUnitario = parseFloat(selectedOption.data('precio')) || 0;
        const stock = parseInt(selectedOption.data('stock')) || 0;
        const cantidad = parseInt(cantidadInput.val());

        if (!productoId || !cantidad || cantidad <= 0) {
            alert("Selecciona un producto y una cantidad válida");
            return;
        }

        if (cantidad > stock) {
            alert(`No hay suficiente stock de ${productoNombre}. Disponible: ${stock}`);
            return;
        }

        const subtotal = precioUnitario * cantidad;

        const row = $(`
            <tr>
                <td>${productoNombre}</td>
                <td>${cantidad}</td>
                <td>$${precioUnitario.toFixed(2)}</td>
                <td>$${subtotal.toFixed(2)}</td>
                <td><button type="button" class="remove-btn">Eliminar</button></td>
            </tr>
        `);
        tableBody.append(row);

        const inputProd = $(`<input type="hidden" name="productos[]" value="${productoId}">`);
        const inputCant = $(`<input type="hidden" name="cantidades[]" value="${cantidad}">`);
        hiddenFields.append(inputProd, inputCant);

        $('#producto-input').val(null).trigger('change');
        cantidadInput.val('');

        row.find('.remove-btn').on('click', function() {
            row.remove();
            inputProd.remove();
            inputCant.remove();
        });
    });

    // 👉 Validación antes de enviar el formulario
    $('#pedido-form').on('submit', function(e) {
        if ($('#hidden-fields input[name="productos[]"]').length === 0) {
            e.preventDefault();
            alert("Debes agregar al menos un producto antes de guardar el pedido");
        }
        
    });
});