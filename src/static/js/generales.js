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
document.addEventListener("DOMContentLoaded", function () {
    const rowsPerPage = 5; // Número de filas por página
    const tableBody = document.getElementById("ventas-body");
    const rows = Array.from(tableBody.querySelectorAll("tr"));
    const paginationControls = document.getElementById("pagination-controls");

    let currentPage = 1; // Página inicial

    // Función para mostrar las filas correspondientes a la página actual
    function displayPage(page) {
        const startIndex = (page - 1) * rowsPerPage;
        const endIndex = startIndex + rowsPerPage;

        rows.forEach((row, index) => {
            row.style.display = index >= startIndex && index < endIndex ? "" : "none";
        });
    }

    // Función para crear los controles de paginación
    function setupPagination() {
        const totalPages = Math.ceil(rows.length / rowsPerPage);
        paginationControls.innerHTML = ""; // Limpiar controles previos

        // Crear botones de paginación
        for (let i = 1; i <= totalPages; i++) {
            const button = document.createElement("button");
            button.textContent = i;
            button.className = "btn-enlace"; // Mantener el estilo original
            button.style.margin = "0 5px"; // Ajustar la separación entre botones

            button.addEventListener("click", () => {
                currentPage = i;
                displayPage(currentPage);

                // Resaltar el botón activo
                Array.from(paginationControls.children).forEach((btn) =>
                    btn.classList.remove("active")
                );
                button.classList.add("active");
            });

            // Resaltar la página inicial
            if (i === currentPage) button.classList.add("active");

            paginationControls.appendChild(button);
        }
    }

    // Inicializar la tabla y los controles de paginación
    displayPage(currentPage);
    setupPagination();
});

document.addEventListener("DOMContentLoaded", () => {
    const botonesFactura = document.querySelectorAll(".ver-factura");
    botonesFactura.forEach((boton) => {
        boton.addEventListener("click", async () => {
            const idVenta = boton.getAttribute("data-id-venta");
            try {
                const response = await fetch(`/obtener_pago/${idVenta}`);
                const data = await response.json();
                if (data.status === "success") {
                    const pago = data.pago;
                    Swal.fire({
                        title: `Factura y Pago - Venta #${pago.id_venta}`,
                        html: `
                            <strong>Número de Factura:</strong> ${pago.numero_factura || "No disponible"}<br>
                            <strong>Monto:</strong> $${pago.monto.toFixed(2)}<br>
                            <strong>Fecha de Pago:</strong> ${pago.fecha_pago}<br>
                            <strong>Hora de Pago:</strong> ${pago.hora_pago}<br>
                            <strong>Nota:</strong> ${pago.nota || "Sin nota"}<br>
                            <strong>ID Pago:</strong> ${pago.id_pagos}<br>
                            <strong>ID Factura:</strong> ${pago.id_factura || "No disponible"}<br>
                        `,
                        icon: "info",
                        confirmButtonText: "Cerrar",
                        customClass: {
                            popup: "swal-wide",
                        },
                    });
                } else {
                    Swal.fire({
                        title: "Error",
                        text: data.message,
                        icon: "error",
                        confirmButtonText: "Cerrar",
                    });
                }
            } catch (error) {
                console.error("Error al obtener los datos:", error);
                Swal.fire({
                    title: "Error",
                    text: "Ocurrió un error al procesar la solicitud.",
                    icon: "error",
                    confirmButtonText: "Cerrar",
                });
            }
        });
    });

    // Search functionality
    const searchInput = document.getElementById('searchInput');
    const ventasTable = document.getElementById('ventasTable');
    const rows = ventasTable.getElementsByTagName('tr');

    searchInput.addEventListener('keyup', function() {
        const filter = searchInput.value.toLowerCase();
        for (let i = 1; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName('td');
            let match = false;
            for (let j = 0; j < cells.length; j++) {
                if (cells[j].innerText.toLowerCase().includes(filter)) {
                    match = true;
                    break;
                }
            }
            rows[i].style.display = match ? '' : 'none';
        }
    });
});

