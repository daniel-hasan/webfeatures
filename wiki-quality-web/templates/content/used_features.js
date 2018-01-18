class Feature {
    constructor(name, description, is_configurable, arrParams) {
        this.name = name; 
        this.description = description;
        this.is_configurable = is_configurable;
        this.arrParams = arrParams;
    }
};

let name = "";
let description = "";
let is_configurable = false;
let arrParams = [];
let arrFeatures = new Array();

{% for key, arr_args in object_list.items %}
{% for arg in arr_args %}

	

	{% ifequal arg['nam_argument'] "name" %}
		name = {{ arg['val_argument'] }};		
	{% endif %}


{% endfor %}
{% endfor %}

{% for feature in object_list %}
	name = "";
	description = "";
	arrParams = [];
	is_configurable = false;
	
	teste = 
	name = "{{ feature.used_feature__feature_set__nam_feature_set }}";
	description = "{{ feature.used_feature__feature_set__dsc_feature_set }}";
	is_configurable = "{{ feature.is_configurable }}";
	
	arrParams.push({'nam_argument' : "{{ feature.nam_argument }}",'val_argument' : "{{ feature.val_argument }}"});
	arrFeatures.push(new Feature(name, description, is_configurable, arrParams));		
{% endfor %}

function insereFeature(feature) {
	let HTMLEl_temp_ul_pai = document.querySelector('#div');
	let HTMLEl_temp_li_feature_set = document.createElement('li');
	let HTMLEl_temp_button = document.createElement('button');
	let HTMLEl_temp_button_is_configurable = document.createElement('button');

	HTMLEl_temp_li_feature_set.id = 'li'
	
	HTMLEl_temp_li_feature_set.innerHTML = feature.name;
	HTMLEl_temp_li_feature_set.title = feature.description;
	
	HTMLEl_temp_button.innerHTML = '';
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
		
		let dialogg;
		  
	    dialogg = $( "#is-configurable-form" ).dialog({
	      autoOpen: false,
	      height: 300,
	      width: 600,
	      modal: true,
	    });
		
		$( ".isConfigurable" ).button().on( "click", function() {
	      dialogg.dialog( "open" );
	    });
	});

	if(feature.is_configurable == 'True'){
		HTMLEl_temp_li_feature_set.appendChild(HTMLEl_temp_button_is_configurable);
	}
	
	HTMLEl_temp_li_feature_set.appendChild(HTMLEl_temp_button);
	HTMLEl_temp_ul_pai.appendChild(HTMLEl_temp_li_feature_set);
}

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


