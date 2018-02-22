//Adiciona uma ação que pode impedir o submit do form quando o botão de submit é apertado.
$(".form").submit(function() {
	//Se o input onde se adiciona o arquivo estiver vazio, retorna falso, impedindo o submit do form, e mostra uma mensagem na tela.
	if($(".dataset-file").val() == '') {
		alert("There isn't a file selected.");
		return false;
	}
	
	//Se a extensão do arquivo não for zip, o formulário não é enviado.
	if($(".dataset-file").val().split('.').pop() != "zip") {
		alert("The file must be a ZIP.");
		return false;
	}
	
	//Se o tamanho (em bytes) do arquivo for maior que o limite, retorna falso.
	if($(".dataset-file")[0].files[0].size > 10*(1024*1024)) {
		alert("The file's size is higher than the limit.");
		return false;
	}
})