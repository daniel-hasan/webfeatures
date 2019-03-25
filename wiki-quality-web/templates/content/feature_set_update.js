{% load static %}

let boolChanged = false;

let href_button_clicked = "";
let boolSave = {% if object.id %}true{%else%}false{%endif%};
let boolRedirectAfterSave = false;
let validationFirstTime = true;
let boolActivated = false;
/******************************** Inicialização ****************************************/
$( function() {

		$("#updateFeatureForm input").focus(function(){
			boolChanged = true;
		});
	    $( "#tabs" ).tabs({
			activate: function( event, ui ) {
				if(boolActivated){
					boolActivated = false;
					return;
				}
				if (boolChanged) {

					if(evaluatesData()){
						salveData();
					} else {
						setTabDescription();
						alert("Invalid input! You must correct it to save the changes.");
					}
				}

			}
		});
		$("#alertInvalidInput").dialog({
			    autoOpen: false,
			    modal: true,
			    title: 'Invalid Input',
			    width: 400,
			    height: 'auto',
			    buttons: {
			        "Fix it": function() {
			          	$( this ).dialog( "close" );
          	},

			        "Exit without saving": function() {
			          	window.location.href = href_button_clicked;
			          	$( this ).dialog( "close" );
			          }
			      }
			 	});
		$("#alertSaveFeature").dialog({
			    autoOpen: false,
			    modal: true,
			    title: 'Configure Feature Set ',
			    width: 400,
			    height: 'auto',
			    buttons: {
			        "Yes": function() {
			          	salveData();
			          	boolRedirectAfterSave = true;
			          	$( this ).dialog( "close" );
          	},

			        "No": function() {
			          	window.location.href = href_button_clicked;
			          	$( this ).dialog( "close" );
			          }
			      }
			 	});

		$("#id_language").attr("required",false);
	});


/********************************* Funções ***********************************************/
function setTabDescription(){
	boolActivated = true;
	$('#tabs').tabs("option","active",0);
}
function cancelEditFeature(){
		window.location.href = '{% url "feature_set_list" %}';
}
function evaluatesData(){
			let nam_f = $('#id_nam_feature_set').val();
			let language_f = $('#id_language').val();
			if(nam_f != "" && language_f != ""){
				return true;
			}
			return false;
}

function salveData(){
			let idNamFeaturesSet = $("#last_saved_name")[0].value;
		  	let arrElementsFeatureSet = [];
		  	let arrCreateElementsFeatureSet = [];

			arrElementsFeatureSet.push({"id_nam_feature_set":idNamFeaturesSet,
										"nam_feature_set": $('#id_nam_feature_set').val(),
										"dsc_feature_set":$('#id_dsc_feature_set').val(),
										"language":$('#id_language').val(),
										"bol_is_public":$("#id_bol_is_public")[0].checked});
			if(boolSave){

				updateFeatureSet(arrElementsFeatureSet);

			}else{
				createFeatureSet(arrElementsFeatureSet);
	  		}
}
function alertSaveFeatures(modificador, hreffinal){
			href_button_clicked = "";



				href_button_clicked = hreffinal

				if(evaluatesData()){
					$("#palertSaveFeature").html('<p>Do you want to save your changes?</p>');
					$( "#alertSaveFeature" ).dialog( "open" );
				} else {
					$("#alertInvalidInput").html('<p>Invalid input! if you want to access '+ hreffinal +' you must correct it.</p>');
					$( "#alertInvalidInput" ).dialog( "open" );
				}

}

function changeShareURL(){
  			let strFeatureSetName = $("#id_nam_feature_set")[0].value;
			  $("#pub_feat_set_name").html(strFeatureSetName);
			  $("#anc")[0].href = "{% url "public_extract_features" user.get_username "" %}"+strFeatureSetName;
}
/************************** AJAX **************************************/
function createFeatureSet(arrCreateElementsFeatureSet){
			$.ajax({
				  url: "{% url "feature_set_insertAJAX" %}",
				  dataType: 'json',
				  type: "POST",
			  	  data: { "arrCreateElementsFeatureSet" : JSON.stringify(arrCreateElementsFeatureSet)},
				  success: function(response) {
				  		if(response.arrErr != ""){
				  			//$('#FeaturesSets').addClass("disabled");
				  			$(".error-container").append( "<p>Error! "+ response.arrErr +"</p>" );
				  			$(".error-container").removeClass("hideGif");
				  			$("#gif").addClass("hideGif");
				  			setTimeout(function(){
				          		$(".error-container").addClass("hideGif");
				        	}, 5000);
							setTabDescription();
				  		} else {
				  			$('#FeaturesSets').removeClass("enable");
					  		$("#last_saved_name")[0].value = response.arrCreateFeatureSet["nam_feature_set"];
					  		gUsedFeaturesNames = {};
					  		changeShareURL();
					  		$("#sharing_link").removeClass("invisible");
					  		if(boolRedirectAfterSave){
									window.location.href = href_button_clicked;
					  		}
							setTimeout(function(){
					  		    $(".success").removeClass("hideGif");
				          		$("#gif").addClass("hideGif");
				        	}, 1000);
				        	setTimeout(function(){
				          		$(".success").addClass("hideGif");
				        	}, 5000);
				        	boolSave = true;
				        	boolChanged = false;
				  		}
				  },
				  error: function(xhr,status,error){
				  		alert("An error occured when trying to save the new configurations:\n"+error);
				  		$("#gif").addClass("hideGif");
		       	  }
				});
		}

function updateFeatureSet(arrElementsFeatureSet){
			$.ajax({
				  url: "{% url "feature_set_editAJAX" %}",
				  dataType: 'json',
				  type: "POST",
			  	  data: { "arrEditElementsFeatureSet" : JSON.stringify(arrElementsFeatureSet)},
				  success: function(response) {
				  		if(response.arrErr != ""){
				  			//$('#FeaturesSets').addClass("disabled");
				  			$(".error-container").append( "<p>Error! "+ response.arrErr +"</p>" );
				  			$(".error-container").removeClass("hideGif");
				  			$("#gif").addClass("hideGif");
				  			setTimeout(function(){
				          		$(".error-container").addClass("hideGif");
				        	}, 5000);
				        	setTabDescription();
				  		} else {
					  		changeShareURL();
								if(boolRedirectAfterSave){
									window.location.href = href_button_clicked;
					  		}
								$("#last_saved_name")[0].value = response.arrFeauteSetEdit["nam_feature_set"];
					  		setTimeout(function(){
				          		$(".success").removeClass("hideGif");
				          		$("#gif").addClass("hideGif");
				        	}, 1000);

				        	setTimeout(function(){
				          		$(".success").addClass("hideGif");
				        	}, 5000);
				        	boolChanged = false;
				        }
				  },
				  error: function(xhr,status,error){
						alert("An error occured when trying to save the new configurations:\n"+error);
		       	  		$("#gif").addClass("hideGif");
		       	  }
				});
		}



/****************** Eventos ************************************/

$("#saveButton").click(function() {
  			if(!evaluatesData()){
  				href_button_clicked = '{% url "feature_set_list"%}';
  				$("#alertInvalidInput").html('<p>Invalid input! You must correct it to save the changes.</p>');
				$( "#alertInvalidInput" ).dialog( "open" );
  			} else {
	  			$("#gif").removeClass("hideGif");
	  			$("#gif").attr("src","{% static "imgs/ajax-loader.gif" %}");
	  			salveData();
  			}
		});


$( "#configureFeatureSet" ).click(function() {

			if (boolChanged) {
				$(this).removeAttr( "href" );
				alertSaveFeatures("configureFeatureSet", '{% url "feature_set_list"%}');
	 		}
});

$( "#analyseTexts" ).click(function() {
	 		if (boolChanged) {
	 			$(this).removeAttr( "href" );
				alertSaveFeatures("analyseTexts", '{% url "extract_features"%}');
			}
});
