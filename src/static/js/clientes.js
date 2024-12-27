// Esperar a que el DOM esté listo
document.addEventListener("DOMContentLoaded", () => {
    // Variables globales
    const userRole = window.userRole || null; // Asegúrate de definir `userRole` en el HTML antes de cargar este script.

    // Obtener el CSRF token
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    // Función para eliminar un cliente
    function deleteClient(clienteId) {
        if (userRole !== 'admin') {
            swal.fire({
                title: 'Error',
                text: 'No tienes permiso para eliminar clientes',
                icon: 'error',
                confirmButtonText: 'OK'
            });
            return;
        }

        swal.fire({
            title: '¿Estás seguro?',
            text: 'Esta acción eliminará el cliente permanentemente. ¿Estás seguro de que deseas continuar?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: 'Sí, eliminar',
            cancelButtonText: 'Cancelar'
        }).then((result) => {
            if (result.isConfirmed) {
                fetch(`/eliminar_cliente/${clienteId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    }
                })
                .then(response => {
                    if (!response.ok) {
                        return response.json().then(data => {
                            throw new Error(data.message || 'Error desconocido');
                        });
                    }
                    return response.json();
                })
                .then(data => {
                    swal.fire('¡Eliminado!', data.message, 'success')
                        .then(() => location.reload());
                })
                .catch(error => {
                    console.error('Error:', error);
                    swal.fire({
                        title: 'Error',
                        text: error.message,
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                });
            }
        });
    }

    // Mostrar modal para editar cliente
    function showEditClientModal(id, nombres, apellidos, direccion, telefono, correo, cedula) {
        Swal.fire({
            title: 'Editar Cliente',
            html: `
                <input id="edit_NameClient" class="swal2-input" placeholder="Nombres" value="${nombres}">
                <input id="edit_LastNameClient" class="swal2-input" placeholder="Apellidos" value="${apellidos}">
                <input id="edit_addressClient" class="swal2-input" placeholder="Dirección" value="${direccion}">
                <input id="edit_phoneClient" type="tel" class="swal2-input" placeholder="Teléfono" value="${telefono}">
                <input id="edit_emailClient" class="swal2-input" placeholder="Correo Electrónico" value="${correo}">
                <input id="edit_cedulaClient" class="swal2-input" placeholder="Cédula" value="${cedula}">
            `,
            focusConfirm: false,
            preConfirm: () => {
                const nombres = document.getElementById('edit_NameClient').value;
                const apellidos = document.getElementById('edit_LastNameClient').value;
                const direccion = document.getElementById('edit_addressClient').value;
                const telefono = document.getElementById('edit_phoneClient').value;
                const correo = document.getElementById('edit_emailClient').value;
                const cedula = document.getElementById('edit_cedulaClient').value;

                // Validación de los campos
                const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
                const phonePattern = /^[0-9]{7,15}$/;

                if (!nombres || !apellidos || !direccion || !telefono || !correo || !cedula) {
                    Swal.showValidationMessage('Por favor, completa todos los campos');
                    return false;
                }

                if (!emailPattern.test(correo)) {
                    Swal.showValidationMessage('Por favor, ingresa un correo electrónico válido');
                    return false;
                }

                if (!phonePattern.test(telefono)) {
                    Swal.showValidationMessage('Por favor, ingresa un número de teléfono válido (7 a 15 dígitos)');
                    return false;
                }

                return fetch('/editar_cliente', {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: new URLSearchParams({
                        cliente_id: id,
                        edit_NameClient: nombres,
                        edit_LastNameClient: apellidos,
                        edit_addressClient: direccion,
                        edit_phoneClient: telefono,
                        edit_emailClient: correo,
                        edit_cedulaClient: cedula,
                    })
                }).then(response => {
                    if (!response.ok) {
                        throw new Error('Error al actualizar el Cliente');
                    }
                    return response.json();
                });
            }
        }).then((result) => {
            if (result.isConfirmed) {
                if (result.value.success) {
                    Swal.fire('Éxito', 'Cliente actualizado correctamente', 'success').then(() => location.reload());
                } else {
                    Swal.fire('Error', 'No se pudo actualizar el cliente', 'error');
                }
            }
        }).catch(error => {
            Swal.fire('Error', error.message, 'error');
        });
    }

    // Validación del campo de teléfono
    const phoneInput = document.getElementById("phoneClient");
    if (phoneInput) {
        phoneInput.addEventListener("keydown", (event) => {
            if (!(event.key >= "0" && event.key <= "9") &&
                !["Backspace", "Delete", "ArrowLeft", "ArrowRight", "Tab", "Home", "End"].includes(event.key)) {
                event.preventDefault();
            }
        });
    }

    // Búsqueda de clientes
    const searchInput = document.getElementById('searchClient');
    if (searchInput) {
        searchInput.addEventListener('input', () => {
            const searchValue = searchInput.value.toLowerCase();
            const clientItems = document.querySelectorAll('.cliente-item');

            clientItems.forEach((clientItem) => {
                const clientName = clientItem.querySelector('.mdl-list__item-sub-title').textContent.toLowerCase();
                clientItem.style.display = clientName.includes(searchValue) ? '' : 'none';
            });
        });
    }

    // Mostrar compras del cliente
    async function mostrarComprasCliente(clienteId) {
        try {
            const response = await fetch(`/mostrar_compras_cliente/${clienteId}`);
            if (!response.ok) throw new Error(`Error: ${response.statusText}`);
            const result = await response.json();

            if (!result.success) {
                Swal.fire('Error', result.message || 'No se pudieron obtener las compras.', 'error');
                return;
            }

            const compras = result.compras;
            if (compras.length === 0) {
                Swal.fire('Sin compras', 'Aún no hay compras realizadas por el cliente.', 'info');
                return;
            }

            const listaHTML = compras.map(venta => `
                <li>
                    <strong>Producto:</strong> ${venta.producto}<br>
                    <strong>Total:</strong> $${(venta.precio_unitario * venta.cantidad_comprada).toFixed(2)}
                </li>
            `).join('');

            Swal.fire({
                title: 'Compras del cliente',
                html: `<ul>${listaHTML}</ul>`,
                icon: 'info'
            });
        } catch (error) {
            Swal.fire('Error', 'No se pudieron obtener las compras.', 'error');
        }
    }
});
