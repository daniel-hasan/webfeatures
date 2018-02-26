//Cria uma classe para organizar as features.
class Feature {
    constructor(feature_set, ord_feature) {
        this.feature_set = feature_set;
        this.ord_feature = ord_feature;     
    }
};

// CÓDIGO DE TESTE

//Cria um novo array onde serão armazenadas as features.
let arrFeatures = new Array();

//Coloca as features existentes dentro do arrFeatures.
{% for feature in object_list %}
    arrFeatures.push(new Feature("{{ feature.feature_set }}", "{{ feature.ord_feature }}"));
{% endfor %}

function insereFeature(feature) {
    //Obtém elemento (div) que servirá de base para a criação do elemento pai onde serão colocados os elementos filhos (características da feature).
    let HTMLEl_temp_ul_pai = document.querySelector('#div');

    //Cria os elementos filhos, onde serão armazenadas as características da feature.
    let HTMLEl_temp_li_feature_set = document.createElement('li');
    
    //Cria um botão que será adicionado após os elementos e que, quando clicado, removerá o elemento pai e todos os filhos.
    let HTMLEl_temp_button = document.createElement('button');
    let HTMLEl_temp_button_is_configurable = document.createElement('button');
    
	HTMLEl_temp_li_feature_set.id = 'li';
	
	let HTMLEl_temp = feature.feature_set;
	
	HTMLEl_temp  = HTMLEl_temp.split("|||");
	
	HTMLEl_temp_li_feature_set.innerHTML  = HTMLEl_temp[0]; 
	HTMLEl_temp_li_feature_set.title  = HTMLEl_temp[1];
    
    //Coloca o inneHTML do botão como "Remove feature".
    HTMLEl_temp_button.innerHTML = "";

    //Adiciona uma classe ao botão criado.
    HTMLEl_temp_button.setAttribute('class', 'button-remove-feature');
    HTMLEl_temp_button_is_configurable.setAttribute('class', 'isConfigurable');
    
    $( function() {
		$('.button-remove-feature').button( {
	        icon: "ui-icon-closethick",
	        iconPosition: "bottom"
	    });
	
		$('.isConfigurable').button( {
		   icon: "ui-icon-gear",
		   iconPosition: "bottom"
		});
		
		$("#div").sortable();
	});
	
	HTMLEl_temp_li_feature_set.appendChild(HTMLEl_temp_button);
	HTMLEl_temp_ul_pai.appendChild(HTMLEl_temp_li_feature_set);
    
}

//Cria uma função para remover a feature.
function remove_feature(e) {
    //Obtém o elemento pai do button, que será o ul criado anteriormente (HTMLEl_temp_ul_pai).
    ul_pai = e.currentTarget.parentNode;
    
    //Pega o pai do ul criado anteriormente (HTMLEl_temp_ul_pai) para remover o filho (elemento pai do button selecionado, HTMLEl_temp_ul_pai).
    ul_pai.parentNode.removeChild(ul_pai);
}

//Insere todos os elementos do arrFeatures na página HTML.
arrFeatures.forEach(insereFeature);

//Obtém todos os botões criados.
let Arr_button = document.querySelectorAll(".button-remove-feature");

//Aciona a função remove_feature para o botão do Arr_button que foi clicado.
for(let cont =  0; cont < Arr_button.length; cont++) {
    Arr_button[cont].addEventListener('click', function(e) {
        remove_feature(e);
});

}