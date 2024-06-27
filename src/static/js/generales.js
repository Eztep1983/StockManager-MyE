// logout.js
document.addEventListener('DOMContentLoaded', function() {
    // Esperar a que el DOM esté completamente cargado
    var logoutLink = document.getElementById('logoutLink');
    if (logoutLink) {
        logoutLink.addEventListener('click', function(event) {
            event.preventDefault(); // Prevenir el comportamiento predeterminado del enlace

            Swal.fire({
                title: '¿Estás seguro?',
                text: "¿Quieres cerrar sesión?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Sí, cerrar sesión'
            }).then((result) => {
                if (result.isConfirmed) {
                    // Redirigir a la ruta de logout después de confirmar
                    window.location.href = event.target.href;
                }
            });
        });
    }
});


// 
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