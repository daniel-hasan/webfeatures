class Feature {
    constructor(name, id, description, is_configurable, arrParams) {
        this.name = name;
        this.id = id;
        this.description = description;
        this.is_configurable = is_configurable;
        this.arrParams = arrParams;
    }
};


var gUsedFeaturesNames = {}
let arrFeaturesToForm = [];

function insereFeature(feature) {
	gUsedFeaturesNames[feature.name] = true;
	let HTMLEl_temp_ul_pai = document.querySelector('#div');
	let HTMLEl_temp_li_feature_set = document.createElement('li');
	let HTMLEl_temp_button = document.createElement('button');
	let HTMLEl_temp_button_is_configurable = document.createElement('button');
	
	HTMLEl_temp_li_feature_set.id = 'li';
	
	HTMLEl_temp_li_feature_set.innerHTML = feature.name;
	HTMLEl_temp_li_feature_set.title = feature.description;
	
	HTMLEl_temp_button.innerHTML = '';
	HTMLEl_temp_button.setAttribute('class', 'button-remove-feature');
	HTMLEl_temp_button_is_configurable.setAttribute('class', 'isConfigurable');	
	
	//Array necessário porque o push do arrFeatures via Ajax só funcionaria depois da página ser recarregada
	arrFeaturesToForm.push(new Feature(feature.name, feature.id, feature.description, feature.is_configurable, feature.arrParams));		

	$(HTMLEl_temp_button).button( {
		icon: "ui-icon-closethick",
	        iconPosition: "bottom"
	});
	    
	HTMLEl_temp_button.addEventListener('click', function(e) {
        	remove_feature(e, feature.id, feature.name);
    });
		
	HTMLEl_temp_button_is_configurable.addEventListener('click', function(e) {
			call_form(HTMLEl_temp_button_is_configurable.id);
		
	});
	
	$("#div").sortable();		
	
	if(feature.is_configurable){
		HTMLEl_temp_button_is_configurable.id = feature.id;
	
			$(HTMLEl_temp_button_is_configurable).button( {
			   icon: "ui-icon-gear",
			   iconPosition: "bottom"
			});
		
		HTMLEl_temp_li_feature_set.appendChild(HTMLEl_temp_button_is_configurable);		
	}
	
	HTMLEl_temp_li_feature_set.appendChild(HTMLEl_temp_button);
	HTMLEl_temp_ul_pai.appendChild(HTMLEl_temp_li_feature_set);
}

function call_form(idForm){

        create_form_feature_is_configurable('form'+idForm, idForm);	
         
	    $( function() {
	         $( HTMLEl_temp_div_is_configurable_form ).dialog({
			    autoOpen: false,
			    modal: true,
			    title: 'Configure Feature: ' + HTMLEl_temp_label_form.innerHTML,
			    width: 400, 
			    height: 'auto',
			    fluid: true, 
			    resizable: false
			 });
			
			$( HTMLEl_temp_div_is_configurable_form ).dialog( "open" ); 
			
			$(window).resize(function () {
			    fluidDialog();
			});
			
			// catch dialog if opened within a viewport smaller than the dialog width
			$(document).on("dialogopen", ".ui-dialog", function (event, ui) {
			    fluidDialog();
			});
			
			function fluidDialog() {
			    var $visible = $(".ui-dialog:visible");
			    $visible.each(function () {
			        var $this = $(this);
			        var dialog = $this.find(".ui-dialog-content").data("ui-dialog");
			        if (dialog.options.fluid) {
			            var wWidth = $(window).width();
			            if (wWidth < (parseInt(dialog.options.maxWidth) + 50))  {
			                $this.css("max-width", "90%");
			            } else {
			                $this.css("max-width", dialog.options.maxWidth + "px");
			            }
			            dialog.option("position", dialog.options.position);
			        }
			    });
			}			
		});	

}
function call_form(idForm){

        create_form_feature_is_configurable('form'+idForm, idForm);	
         
	    $( function() {
	         $( HTMLEl_temp_div_is_configurable_form ).dialog({
			    autoOpen: false,
			    modal: true,
			    title: 'Configure Feature: ' + HTMLEl_temp_label_form.innerHTML,
			    width: 400, 
			    height: 'auto',
			    fluid: true, 
			    resizable: false
			 });
			
			$( HTMLEl_temp_div_is_configurable_form ).dialog( "open" ); 
			
			$(window).resize(function () {
			    fluidDialog();
			});
			
			// catch dialog if opened within a viewport smaller than the dialog width
			$(document).on("dialogopen", ".ui-dialog", function (event, ui) {
			    fluidDialog();
			});
			
			function fluidDialog() {
			    var $visible = $(".ui-dialog:visible");
			    $visible.each(function () {
			        var $this = $(this);
			        var dialog = $this.find(".ui-dialog-content").data("ui-dialog");
			        if (dialog.options.fluid) {
			            var wWidth = $(window).width();
			            if (wWidth < (parseInt(dialog.options.maxWidth) + 50))  {
			                $this.css("max-width", "90%");
			            } else {
			                $this.css("max-width", dialog.options.maxWidth + "px");
			            }
			            dialog.option("position", dialog.options.position);
			        }
			    });
			}			
		});	

}


function create_form_feature_is_configurable(idForms, idButton){	

	let arr_temp_parms = [];
	let featureName = ""
	
	for(let i=0; i<arrFeaturesToForm.length; i++){
		if(arrFeaturesToForm[i].id == idButton){
			featureName = arrFeaturesToForm[i].name;
			arr_temp_parms = arrFeaturesToForm[i].arrParams;
		}
	}
	
	insert_feature_is_configurable(arr_temp_parms, idForms, featureName, idButton);
}


let HTMLEl_temp_div_is_configurable_form =  document.createElement('div');
let HTMLEl_temp_label_form = document.createElement('span');
let posiImagem  = document.createElement('div');
let selectedParams = [];

function insert_feature_is_configurable(arrParams, idDivForms, featureName, used_feature_id){
	selectedParam = [];
	let type_argument = "";
	let val_argument = "";
	let featureLabel = "";
	let id = "";

	HTMLEl_temp_div_is_configurable_form.innerHTML = "";		
	HTMLEl_temp_div_is_configurable_form.id = idDivForms;
	
	HTMLEl_temp_label_form.innerHTML = featureName;			

	let HTMLEl_temp_form = document.createElement('form');	
	let HTMLEl_temp_space = document.createElement('p');		
	let HTMLEl_temp_button_save = document.createElement('button');
	let HTMLEl_temp_button_cancel = document.createElement('button');
	
	posiImagem.innerHTML = "";
			
	//CSRF	token criado aqui por ser um form dinâmico
	let inputCSRF = document.createElement('input');
		
		inputCSRF.type = 'hidden';
		inputCSRF.name = 'csrfmiddlewaretoken';
		inputCSRF.value = '{{ csrf_token }}';
	
	HTMLEl_temp_form.method = 'post';
	HTMLEl_temp_form.appendChild(inputCSRF);
			
	HTMLEl_temp_button_save.innerHTML = 'Save';
	HTMLEl_temp_button_save.setAttribute('type', 'button');
	
	HTMLEl_temp_button_cancel.innerHTML = 'Cancel';
	HTMLEl_temp_button_cancel.setAttribute('type', 'button');
	
	HTMLEl_temp_button_save.setAttribute('class', 'ui-button ui-widget ui-corner-all');
	
	HTMLEl_temp_button_cancel.addEventListener("click",function() {
		$( HTMLEl_temp_div_is_configurable_form ).dialog( "close" );
	});
	
	HTMLEl_temp_button_save.addEventListener("click",function() {
		let arrElements = [];
		for(let intI = 0; intI < selectedParam.length ; intI++){
			posiImagem.appendChild(imagem);
			arrElements.push({"idArgVal":selectedParam[intI].id,"valueArgVal":selectedParam[intI].value});
		}
		create_post(arrElements,used_feature_id);
	});
	
	HTMLEl_temp_button_cancel.setAttribute('class', ' cancelIsConfigurable ui-button ui-widget ui-corner-all');
	
	for(foreignKey in arrParams){
		
		let HTMLEl_temp_label = document.createElement('span');
		let HTMLEl_temp_value_argument = document.createElement('input');
		let elDscArgument = document.createElement('p');
		$(elDscArgument).addClass("infobox");
		$(elDscArgument).addClass("ui-corner-all");
		let bolHasDscArgument = false;
		for(key in arrParams[foreignKey]){
			
			if(key == 'id'){
				id = arrParams[foreignKey][key];
			}
			
			if(key == 'nam_argument'){
				featureLabel = arrParams[foreignKey][key];	
			}
			
			if(key == 'val_argument'){
				val_argument = arrParams[foreignKey][key];		
			}
			
			if(key == 'dsc_argument'){
				elDscArgument.innerHTML = arrParams[foreignKey][key];
				if(arrParams[foreignKey][key].trim().length > 0){
					bolHasDscArgument = true;
				}		
			}
			
			if(key == 'type_argument'){
				type_argument = arrParams[foreignKey][key];	
			}
			
		}
		
		// Add  id input
		argVal_id = parseInt(id, 10);
		HTMLEl_temp_value_argument.setAttribute("id", argVal_id);				
						
		// Add formatação label
		HTMLEl_temp_label.innerHTML = featureLabel + ': ';	
		
		//Add id form
		HTMLEl_temp_form.id = 'form'+used_feature_id;
		
		// Tratando form
			if(type_argument == 'int'){
				
				HTMLEl_temp_value_argument.setAttribute("type", "number");
				HTMLEl_temp_value_argument.value = parseInt(val_argument, 10);
			
			} else if (type_argument == 'string'){
			
				HTMLEl_temp_value_argument.setAttribute("type", "text");
				HTMLEl_temp_value_argument.value = val_argument; 	
			
			} else if (type_argument == 'json'){
			
				alert("json ainda não está sendo tratado.");
			
			}
		selectedParam.push(HTMLEl_temp_value_argument);
			
		HTMLEl_temp_value_argument.setAttribute('class', 'sizeinputs');	
		HTMLEl_temp_label.setAttribute('class', 'labelForm');
		
		HTMLEl_temp_form.appendChild(HTMLEl_temp_label);
		if(bolHasDscArgument){
			HTMLEl_temp_form.appendChild(elDscArgument);
		}
		HTMLEl_temp_form.appendChild(HTMLEl_temp_value_argument);
	}	
		HTMLEl_temp_form.appendChild(HTMLEl_temp_space);
		HTMLEl_temp_form.appendChild(posiImagem);
		HTMLEl_temp_form.appendChild(HTMLEl_temp_button_save);
		HTMLEl_temp_form.appendChild(HTMLEl_temp_button_cancel);
		HTMLEl_temp_div_is_configurable_form.appendChild(HTMLEl_temp_form);	
		    	
}
