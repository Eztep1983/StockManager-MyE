function getCSRFToken(){
    return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
}  

function deleteClient(clienteId) {
            console.log('Cliente ID:', clienteId);  //pa ver si esta cogiendo el id
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

        // Expresiones regulares para validar teléfono y correo electrónico
        const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
        const phonePattern = /^[0-9]{7,15}$/;

        // Verificación para campos vacíos
        if (!nombres || !apellidos || !direccion || !telefono || !correo || !cedula) {
            Swal.showValidationMessage('Por favor, completa todos los campos');
            return false;
        }
        if (telefono < 0 || cedula < 0){
            Swal.showValidationMessage("Solo puedes agregar numeros positivos")
            return false
        }

        // Validación del formato de correo electrónico
        if (!emailPattern.test(correo)) {
            Swal.showValidationMessage('Por favor, ingresa un correo electrónico válido');
            return false;
        }

        // Validación del formato de teléfono (solo números de 7 a 15 dígitos)
        if (!phonePattern.test(telefono)) {
            Swal.showValidationMessage('Por favor, ingresa un número de teléfono válido (7 a 15 dígitos)');
            return false;
        }

        // Llamada a la ruta de edición
        return fetch('/editar_cliente', {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': document.querySelector('meta[name="csrf-token"]').getAttribute('content')
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
      
    document.addEventListener("DOMContentLoaded", function() {
        // Obtener el icono de búsqueda
        var searchIcon = document.getElementById("searchIcon");
    
        // Agregar evento click al icono de búsqueda
        searchIcon.addEventListener("click", function() {
            // Obtener la barra de navegación
            var navigationBar = document.querySelector(".mdl-navigation");
    
            // Mostrar u ocultar la barra de navegación cambiando la clase CSS
            if (navigationBar.classList.contains("show-navigation")) {
                // Si la barra de navegación está visible, ocultarla
                navigationBar.classList.remove("show-navigation");
            } else {
                // Si la barra de navegación está oculta, mostrarla
                navigationBar.classList.add("show-navigation");
            }
        });
    });            
    // Agregar evento submit al formulario de edición
document.addEventListener("DOMContentLoaded", function() {
    var editForms = document.querySelectorAll('[id^="editForm"]');
    editForms.forEach(function(form) {
        form.addEventListener("submit", function(event) {
            // Evitar que el formulario se envíe automáticamente
            event.preventDefault();
            
            // Enviar el formulario manualmente utilizando Fetch API o AJAX
            var formId = form.getAttribute("id");
            var formData = new FormData(form);
            fetch('/editar_cliente', {
                method: 'POST',
                body: formData
            })
            .then(function(response) {
                // Verificar si la respuesta fue exitosa
                if (response.ok) {
                    // Recargar la página y mostrar la alerta
                    reloadPageAndShowAlert();
                } else {
                    // Mostrar mensaje de error si la respuesta no fue exitosa
                    swal.fire({
                        title: 'Error',
                        text: 'Hubo un problema al actualizar el cliente. Por favor, inténtalo de nuevo.',
                        icon: 'error',
                        confirmButtonText: 'OK'
                    });
                }
            })
            .catch(function(error) {
                console.error('Error:', error);
                // Mostrar mensaje de error en caso de error en la solicitud
                swal.fire({
                    title: 'Error',
                    text: 'Hubo un problema al actualizar el cliente. Por favor, inténtalo de nuevo.',
                    icon: 'error',
                    confirmButtonText: 'OK'
                });
            });
        });
    });
});        
document.getElementById("btn-addClient").addEventListener("click", function(event) {
    // Evita que el formulario se envíe automáticamente
    event.preventDefault();

    // Validar que todos los campos obligatorios estén llenos
    var dni = document.getElementById("DNIClient").value.trim();
    var nombre = document.getElementById("NameClient").value.trim();
    var apellido = document.getElementById("LastNameClient").value.trim();
    var direccion = document.getElementById("addressClient1").value.trim();
    var telefono = document.getElementById("phoneClient").value.trim();
    var email = document.getElementById("emailClient").value.trim();

    if (dni === "" || nombre === "" || apellido === "" || direccion === "" || telefono === "" || email === "") {
        // Mostrar mensaje de advertencia si algún campo está vacío
        swal.fire({
            title: '¡Advertencia!',
            text: 'Por favor completa todos los campos antes de agregar el cliente.',
            icon: 'warning',
            confirmButtonText: 'OK'
        });
    } else {
        // Mostrar confirmación y enviar el formulario si todos los campos están llenos
        swal.fire({
            title: '¡Se guardó el cliente con éxito!',
            icon: 'success',
            confirmButtonText: 'OK',
            showCancelButton: false
        }).then((result) => {
            // Envía manualmente el formulario solo si el usuario hizo clic en "OK"
            if (result.isConfirmed) {
                document.getElementById("clientForm").submit();  // Envía el formulario con JavaScript
            }
        });
    }
});
document.addEventListener("DOMContentLoaded", function() {
    var secondaryActions = document.querySelectorAll(".mdl-list__item-secondary-action");

    secondaryActions.forEach(function(action) {
        action.addEventListener("click", function(event) {
            var updateOption = action.querySelector(".update-client-option");
            var deleteOption = action.querySelector(".delete-client-option");

            if (updateOption && event.target === updateOption) {
                // Aquí redirige al usuario a la página de actualización del cliente
                window.location.href = "/actualizar-cliente?id=" + clienteId;
            } else if (deleteOption && event.target === deleteOption) {
                // Aquí muestra un mensaje de confirmación antes de borrar el cliente
                if (confirm("¿Estás seguro de que deseas borrar este cliente?")) {
                    // Aquí puedes hacer una solicitud para borrar el cliente del servidor
                }
            }
        });
    });
});  
    // Obtener el campo de teléfono
    var phoneInput = document.getElementById("phoneClient");
    phoneInput.addEventListener("keydown", function(event) {
        // Permitir solo números y teclas especiales como Backspace, Delete, Flechas, etc.
        if (!(event.key >= "0" && event.key <= "9") &&
            event.key !== "Backspace" &&
            event.key !== "Delete" &&
            event.key !== "ArrowLeft" &&
            event.key !== "ArrowRight" &&
            event.key !== "ArrowUp" &&
            event.key !== "ArrowDown" &&
            event.key !== "Tab" &&
            event.key !== "Home" &&
            event.key !== "End") {
            // Evitar la acción predeterminada si la tecla presionada no es un número o una tecla especial permitida
            event.preventDefault();
        }
    });
document.getElementById('searchClient').addEventListener('input', function () {
    const searchValue = this.value.toLowerCase();
    const clientItems = document.querySelectorAll('.cliente-item');

    clientItems.forEach(function (clientItem) {
        const clientName = clientItem.querySelector('.mdl-list__item-sub-title').textContent.toLowerCase();
        if (clientName.includes(searchValue)) {
            clientItem.style.display = '';
        } else {
            clientItem.style.display = 'none';
        }
    });
});
