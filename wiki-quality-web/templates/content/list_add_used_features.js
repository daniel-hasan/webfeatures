/**
 * Format the url template with the language code.
 * @author Daniel Hasan Dalip.
 * @since  09/02/2018
 */
 function format_language_code_url(strTemplateURL,strLanguageCode){
 	return strTemplateURL.replace("__language_code__",strLanguageCode);
 }
 
 /**
 * Format the url template with the feature set name.
 * @author Daniel Hasan Dalip.
 * @since  09/02/2018
 */
 function format_feature_set_url(strTemplateURL,strFeatureSet){
 	return strTemplateURL.replace("__feature_set__",strFeatureSet);
 }
/**
 * Insert all the features. The parameter arrFeaturesNames are the features name (array of string) to add.
 * @author Daniel Hasan Dalip.
 * @since  09/02/2018
 */
function insertFeatures(arrFeaturesNames,strFeatureSet){
	$.ajax({
	  url: format_feature_set_url("{% url "insert_used_features" "__feature_set__" %}",strFeatureSet),
	  dataType: 'json',
	  type: "POST",
  	  data: {"hidUsedFeaturesToInsert": JSON.stringify(arrFeaturesNames)},
	  success: function(response) {
	  let arrNewFeatureInsert = response.arrUsedFeatures;

	  let arrFeatures = [];
	  
	  for(let i = 0; i<arrNewFeatureInsert.length ; i++){
	  	arrFeatures.push(new Feature(arrNewFeatureInsert[i].name, arrNewFeatureInsert[i].used_feature_id, 
	  								arrNewFeatureInsert[i].description, 
	  								arrNewFeatureInsert[i].is_configurable, 
	  								arrNewFeatureInsert[i].arr_param));		
	  }
	  
	  arrFeatures.forEach(insereFeature);
	  
	  },	  
	  error: function(xhr,status,error){
	  	alert("An error occured when trying to insert the features:\n"+error);
	  }
	});
}
/**
 * Insert a feature item on the feature item list
 * @author Daniel Hasan Dalip/Aline Cristina Pinto.
 * @since  09/02/2018
 */

let HTMLEl_temp_div_add_feature = document.createElement('div');
	
function insertNewFeatureItem(objFeatureItem){
	
	if(objFeatureItem.name in gUsedFeaturesNames){
		return;					
	}
	
	let HTMLEl_temp_div = document.querySelector('#add-form');
	
	// list Add Feature
	let HTMLEl_temp_input_checkbox = document.createElement('input');
	let HTMLEl_temp_FeatureItemName = document.createElement('p');
	let HTMLEl_temp_button_save = document.createElement('button');
	let HTMLEl_temp_button_cancel = document.createElement('button');
	
	HTMLEl_temp_button_save.innerHTML = "Save";
	HTMLEl_temp_button_cancel.innerHTML = "Cancel";
	
	HTMLEl_temp_input_checkbox.setAttribute("type", "checkbox");
	HTMLEl_temp_input_checkbox.style.float = "left";
	
	HTMLEl_temp_input_checkbox.value = objFeatureItem.name;
	HTMLEl_temp_FeatureItemName.innerHTML = " "+objFeatureItem.name;
	
	//Alt Description + reference 
	HTMLEl_temp_FeatureItemName.title = objFeatureItem.description + ' | ' + objFeatureItem.reference;

	HTMLEl_temp_div_add_feature.appendChild(HTMLEl_temp_input_checkbox);
	HTMLEl_temp_div_add_feature.appendChild(HTMLEl_temp_FeatureItemName);
	HTMLEl_temp_div.appendChild(HTMLEl_temp_div_add_feature);
	
}
/**
 * Get all the features given the language code
 * @author Daniel Hasan Dalip.
 * @since  09/02/2018
 */
function getFeatureList(domFeatureList,strLanguageCode){
	
	$.ajax({
	  url: format_language_code_url("{% url "list_all_features" "__language_code__" %}",strLanguageCode),
	  dataType: 'json',
	  type: "POST",
	  success: function(response) {
	    let featureList = response.arrFeatures;
	    
		//clean the feature lista data and, for each feature in featureList, insert in insertNewFeatureItem  
		domFeatureList.innerHTML = "";
		let contEncontrouTodos = 0;
		for(intI =0 ; intI<featureList.length ; intI++){
			if(featureList[intI].name in gUsedFeaturesNames){
				contEncontrouTodos++;					
			}
		}
		console.log(contEncontrouTodos);
		if(contEncontrouTodos == featureList.length){
			document.getElementById("add-form").innerHTML = "All the features were used.";	
		}else{
	    	featureList.forEach(insertNewFeatureItem);
	    }    
	    
	  },	  
	  error: function(xhr,status,error){
	  	alert("An error occured during the retrieval of the feature list:\n"+error);
	  }
	});
}
