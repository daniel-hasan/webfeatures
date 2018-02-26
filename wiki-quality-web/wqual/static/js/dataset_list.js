//Só executa o código quando o DOM é carregado.
$(document).ready(function() {
	//Quando um arquivo for adicionado, aparece APENAS o nome dele, sem o fakepath, no span de classe dataset-file-name.
	$("#dataset-file-input").change(function() {
		$(".dataset-file-name").html($("#dataset-file-input")[0].files[0].name);
	});
	
	//Adiciona uma ação que pode impedir o submit do form quando o botão de submit é apertado.
	$(".form").submit(function() {
		var ImpedirSubmit = 'F';
		$('.dataset-error-container').css("display", "none");
		$('.dataset-error-container').empty();
		
		//Se não tiver um arquivo no imput tipo file, adiciona uma mensagem de erro e impede o submit.
		if($("#dataset-file-input").val() == '') {
			$('.dataset-error-container').append("<p>There isn't a file selected.</p>");
			ImpedirSubmit = 'V';
		}
		
		//Se a extensão do arquivo não for zip, adiciona uma mensagem de erro e impede o submit.
		if($("#dataset-file-input").val().split('.').pop() != "zip") {
			$('.dataset-error-container').append("<p>The file must be a ZIP.</p>");
			ImpedirSubmit = 'V';
		}
		
		//Se o tamanho (em bytes) do arquivo for maior que o limite, adiciona uma mensagem e impede o submit.
		if($("#dataset-file-input").val() != '') {
			if($("#dataset-file-input")[0].files[0].size > 10*(1024*1024)) {
				$('.dataset-error-container').append("<p>The file's size is higher than the limit.</p>");
				ImpedirSubmit = 'V';
			}
		}
		
		//Se tiver algum erro, impede o submit do formulário.
		if(ImpedirSubmit == 'V') {
			$('.dataset-error-container').css("display", "block");
			return false;
		}
	});
});