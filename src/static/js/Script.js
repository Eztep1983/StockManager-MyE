var current = null;
document.querySelector('#email').addEventListener('focus', function(e) {
  if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: 0,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '240 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});
document.querySelector('#password').addEventListener('focus', function(e) {
  if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: -336,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '240 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});
document.querySelector('#submit').addEventListener('focus', function(e) {
  if (current) current.pause();
  current = anime({
    targets: 'path',
    strokeDashoffset: {
      value: -730,
      duration: 700,
      easing: 'easeOutQuart'
    },
    strokeDasharray: {
      value: '530 1386',
      duration: 700,
      easing: 'easeOutQuart'
    }
  });
});

// Agregar event listener para el desplazamiento táctil en dispositivos móviles
document.querySelector("nav").addEventListener("touchmove", function(event) {
  event.preventDefault(); // Evita el desplazamiento de la página
  var touch = event.touches[0]; // Obtiene el primer toque
  var startX = touch.clientX; // Posición inicial del toque

  // Agregar event listener para el desplazamiento táctil final
  document.querySelector("nav").addEventListener("touchend", function(event) {
      var touchEnd = event.changedTouches[0]; // Obtiene el toque final
      var endX = touchEnd.clientX; // Posición final del toque

      // Calcula la distancia recorrida por el desplazamiento
      var distance = startX - endX;

      // Determina la dirección del desplazamiento
      if (distance > 50) {
          // Desplazamiento hacia la derecha (cambiar a la siguiente sección)
          window.scrollBy({ left: window.innerWidth, behavior: 'smooth' });
      } else if (distance < -50) {
          // Desplazamiento hacia la izquierda (cambiar a la sección anterior)
          window.scrollBy({ left: -window.innerWidth, behavior: 'smooth' });
      }
  });
});