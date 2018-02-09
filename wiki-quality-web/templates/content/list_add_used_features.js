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
 * Format the feature names to send in post data
 * @author Daniel Hasan Dalip.
 * @since  09/02/2018
 */
 function format_feature_names(arrFeatureNames){
 	let strFeats = "";
 	for(intI = 0; intI<arrFeatureNames.length ; intI++){
 		if(intI != 0){
 			arrFeatureNames += "|";
 		}
 		strFeats += arrFeatureNames[intI]
 	}
 	return strFeats;
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
  	  data: {hidUsedFeaturesToInsert : format_feature_names(arrFeaturesNames)},
	  success: function(response) {
	    //TODO: Chamar a funcao para adicionar a feature no feature set
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
function insertNewFeatureItem(objFeatureItem){
	alert("Nome: "+objFeatureItem.name+
			" description: "+objFeatureItem.description+
			" Reference: "+objFeatureItem.reference);
			
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
	    
		//clean the feature lista data and, for each feature in featureList, insert in   insertNewFeatureItem  
		domFeatureList.innerHTML = "";
	    featureList.forEach(insertNewFeatureItem);
	  },	  
	  error: function(xhr,status,error){
	  	alert("An error occured during the retrieval of the feature list:\n"+error);
	  }
	});
}
