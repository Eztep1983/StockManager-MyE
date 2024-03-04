$(document).ready(function(){
	/*Mostrar ocultar area de notificaciones*/
	$('.btn-Notification').on('click', function(){
        var ContainerNoty=$('.container-notifications');
        var NotificationArea=$('.NotificationArea');
        if(NotificationArea.hasClass('NotificationArea-show')&&ContainerNoty.hasClass('container-notifications-show')){
            NotificationArea.removeClass('NotificationArea-show');
            ContainerNoty.removeClass('container-notifications-show');
        }else{
            NotificationArea.addClass('NotificationArea-show');
            ContainerNoty.addClass('container-notifications-show');
        }
    });
    /*Mostrar ocultar menu principal*/
    $('.btn-menu').on('click', function(){
    	var navLateral=$('.navLateral');
    	var pageContent=$('.pageContent');
    	var navOption=$('.navBar-options');
    	if(navLateral.hasClass('navLateral-change')&&pageContent.hasClass('pageContent-change')){
    		navLateral.removeClass('navLateral-change');
    		pageContent.removeClass('pageContent-change');
    		navOption.removeClass('navBar-options-change');
    	}else{
    		navLateral.addClass('navLateral-change');
    		pageContent.addClass('pageContent-change');
    		navOption.addClass('navBar-options-change');
    	}
    });
    /*Salir del sistema*/
    $('.btn-exit').on('click', function(){
    	swal({
		  	title: 'You want out of the system?',
		 	text: "The current session will be closed and will leave the system",
		  	type: 'warning',
		  	showCancelButton: true,
		  	confirmButtonText: 'Yes, exit',
		  	closeOnConfirm: false
		},
		function(isConfirm) {
		  	if (isConfirm) {
		    	window.location='index.html'; 
		  	}
		});
    });
    /*Mostrar y ocultar submenus*/
    $('.btn-subMenu').on('click', function(){
    	var subMenu=$(this).next('ul');
    	var icon=$(this).children("span");
    	if(subMenu.hasClass('sub-menu-options-show')){
    		subMenu.removeClass('sub-menu-options-show');
    		icon.addClass('zmdi-chevron-left').removeClass('zmdi-chevron-down');
    	}else{
    		subMenu.addClass('sub-menu-options-show');
    		icon.addClass('zmdi-chevron-down').removeClass('zmdi-chevron-left');
    	}
    });
});
(function($){
    $(window).load(function(){
        $(".navLateral-body, .NotificationArea, .pageContent").mCustomScrollbar({
            theme:"dark-thin",
            scrollbarPosition: "inside",
            autoHideScrollbar: true,
            scrollButtons:{ enable: true }
        });
    });
})(jQuery);

function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    if (userInput !== "") {
        displayMessage("user", userInput);
        // Aquí puedes enviar el mensaje del usuario a tu backend para procesarlo con tu IA
        // y recibir la respuesta para mostrarla en el chat
        // Por ahora, simplemente mostraremos una respuesta aleatoria como ejemplo
        var response = getBotResponse(userInput);
        displayMessage("bot", response);
        document.getElementById("user-input").value = "";
    }
}

function displayMessage(sender, message) {
    var chatArea = document.getElementById("chat-area");
    var messageElement = document.createElement("div");
    messageElement.classList.add(sender);
    messageElement.innerText = message;
    chatArea.appendChild(messageElement);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function getBotResponse(userInput) {
    // Esta función simula la respuesta de un bot, puedes reemplazarla con la lógica de tu IA real
    var responses = ["Entiendo, ¿cómo puedo ayudarte?", "¿Hay algo más en lo que pueda asistirte?", "Gracias por tu mensaje. ¿Qué más te gustaría saber?"];
    return responses[Math.floor(Math.random() * responses.length)];
}