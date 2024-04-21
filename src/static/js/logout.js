document.getElementById('logoutLink').addEventListener('click', function(event) {
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