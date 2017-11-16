//Cria uma classe para organizar as features.
class Feature {
	constructor(feature, feature_time_to_extract, feature_visibility) {
		this.feature = feature;
		this.time_to_extract = feature_time_to_extract;
		this.visibility = feature_visibility;
	}
};

//Cria um novo array onde serão armazenadas as features.
let arrFeatures = new Array();

//Coloca as features existentes dentro do arrFeatures.
{% for FeatureSet in UsedFeature %}
	arrFeatures.push(new Feature("{{ FeatureSet.feature }}", "{{ FeatureSet.feature_time_to_extract }}", "{{ FeatureSet.feature_visibility }}"));
{% endfor %}

function insereFeature(feature) {
	//Obtém elemento que servirá de base para a criação do elemento pai onde serão colocados os elementos filhos (características da feature).
	let HTMLEl_temp_body = document.querySelector('body');

	//Cria o elemento pai.
	let HTMLEl_temp_ul = document.createElement('ul');
	
	//Cria os elementos filhos (características da feature).
	let HTMLEl_temp_li_feature = document.createElement('li');
	let HTMLEl_temp_li_feature_time_to_extract = document.createElement('li');
	let HTMLEl_temp_li_feature_visibility = document.createElement('li');

	//Cria um botão que será adicionado após as características da feature e que, quando clicado, removerá a feature.
	let HTMLEl_temp_button = document.createElement('button');
	
	//Coloca o innerHTML de cada filho como o valor de cada uma das características da feature.
	HTMLEl_temp_li_feature = feature.feature;
	HTMLEl_temp_li_feature_time_to_extract = feature.time_to_extract;
	HTMLEl_temp_li_feature_visibility = feature.visibility;

	//Coloca o inneHTML do botão como "Remove feature".
	HTMLEl_temp_button.innerHTML = 'Remove feature';

	//Adiciona uma classe ao botão criado.
	HTMLEl_temp_button.setAttribute('class', 'button-remove-feature');

	//Adiciona o pai.
	HTMLEl_temp_body.appendChild(HTMLEl_temp_ul);

	//Adiciona os filhos.
	HTMLEl_temp_ul.appendChild(HTMLEl_temp_li_feature);
	HTMLEl_temp_ul.appendChild(HTMLEl_temp_li_feature_time_to_extract);
	HTMLEl_temp_ul.appendChild(HTMLEl_temp_li_feature_visibility);
	HTMLEl_temp_ul.appendChild(HTMLEl_temp_button);
}

function remove_feature(e) {
	e.currentTarget.parentNode.remove;
}

//Insere todos os elementos do arrFeatures na página HTML.
arrFeatures.forEach(insereFeature);

let Arr_button = document.querySelectorAll(".button-remove-feature");

for(let button in Arr_button) {
	button.addEventListener('click', remove_feature(button));
}
