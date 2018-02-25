$(".dataset-file-input").change(function() {
	$(".dataset-file-name").textContent = this.value;
});

//Adiciona uma ação que pode impedir o submit do form quando o botão de submit é apertado.
$(".form").submit(function() {
	var ImpedirSubmit = 'F';
	$('.signup-dataset-error-container').css("display", "none");
	$('.signup-dataset-error-container').empty();
	
	//Se não tiver um arquivo no imput tipo file, adiciona uma mensagem de erro e impede o submit.
	if($(".dataset-file-input").val() == '') {
		$('.signup-dataset-error-container').append("<p>There isn't a file selected.</p>");
		ImpedirSubmit = 'V';
	}
	
	//Se a extensão do arquivo não for zip, adiciona uma mensagem de erro e impede o submit.
	if($(".dataset-file-input").val().split('.').pop() != "zip") {
		$('.signup-dataset-error-container').append("<p>The file must be a ZIP.</p>");
		ImpedirSubmit = 'V';
	}
	
	//Se o tamanho (em bytes) do arquivo for maior que o limite, adiciona uma mensagem e impede o submit.
	if($(".dataset-file-input").val() != '') {
		if($(".dataset-file-input")[0].files[0].size > 10*(1024*1024)) {
			$('.signup-dataset-error-container').append("<p>The file's size is higher than the limit.</p>");
			ImpedirSubmit = 'V';
		}
	}
	
	//Se tiver algum erro, impede o submit do formulário.
	if(ImpedirSubmit == 'V') {
		$('.signup-dataset-error-container').css("display", "block");
		return false;
	}
})