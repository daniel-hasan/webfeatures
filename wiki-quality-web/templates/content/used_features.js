//Cria uma classe para organizar as features.
class Feature {
    constructor(feature_set, feature, feature_time_to_extract, feature_visibility) {
        this.feature_set = feature_set;
        this.feature = feature;
        this.feature_time_to_extract = feature_time_to_extract;
        this.feature_visibility = feature_visibility;
    }
};

//Cria um novo array onde serão armazenadas as features.
let arrFeatures = new Array();

//Coloca as features existentes dentro do arrFeatures.
{% for feature in object_list %}
    arrFeatures.push(new Feature("{{ feature.feature_set }}","{{ feature.feature }}", "{{ feature.feature_time_to_extract }}", "{{ feature.feature_visibility }}"));
{% endfor %}

function insereFeature(feature) {
    //Obtém elemento (div) que servirá de base para a criação do elemento pai onde serão colocados os elementos filhos (características da feature).
    let HTMLEl_temp_div = document.querySelector('#div');

    //Cria o elemento pai.
    let HTMLEl_temp_ul_pai = document.createElement('ul');

    //Cria os elementos filhos, onde serão armazenadas as características da feature.
    let HTMLEl_temp_li_feature_set = document.createElement('li');
    let HTMLEl_temp_li_feature = document.createElement('li');
    let HTMLEl_temp_li_feature_time_to_extract = document.createElement('li');
    let HTMLEl_temp_li_feature_visibility = document.createElement('li');

    //Cria um botão que será adicionado após os elementos e que, quando clicado, removerá o elemento pai e todos os filhos.
    let HTMLEl_temp_button = document.createElement('button');

    //Coloca o innerHTML de cada filho como o valor de cada uma das características da feature.
    HTMLEl_temp_li_feature_set.innerHTML = feature.feature_set;
    HTMLEl_temp_li_feature.innerHTML = feature.feature;
    HTMLEl_temp_li_feature_time_to_extract.innerHTML = feature.feature_time_to_extract;
    HTMLEl_temp_li_feature_visibility.innerHTML = feature.feature_visibility;

    //Coloca o inneHTML do botão como "Remove feature".
    HTMLEl_temp_button.innerHTML = "Remove feature";

    //Adiciona uma classe ao botão criado.
    HTMLEl_temp_button.setAttribute('class', 'button-remove-feature');

    //Adiciona o pai.
    HTMLEl_temp_div.appendChild(HTMLEl_temp_ul_pai);

    //Adiciona os filhos.
    HTMLEl_temp_ul_pai.appendChild(HTMLEl_temp_li_feature_set);
    HTMLEl_temp_ul_pai.appendChild(HTMLEl_temp_li_feature);
    HTMLEl_temp_ul_pai.appendChild(HTMLEl_temp_li_feature_time_to_extract);
    HTMLEl_temp_ul_pai.appendChild(HTMLEl_temp_li_feature_visibility);
    HTMLEl_temp_ul_pai.appendChild(HTMLEl_temp_button);
   
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