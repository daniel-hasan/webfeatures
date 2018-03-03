let featName = "";
let id = "";
let featDescription = "";
let is_configurable = false;
let arrParams = [];
let arrFeatures = new Array();
let arr_isConfigurable_form = new Array();

{% for key, arr_args in object_list.items %}
	featName = "";
	featId = "";
	featDescription = "";
	arrParams = [];
	
	{% for arg in arr_args %}			

		is_configurable = false;
	
		{% ifequal arg.nam_argument "name" %}
			featName = "{{ arg.val_argument }}";		
		{% endifequal %}
	
		{% ifequal arg.nam_argument "description" %}
			featDescription = "{{ arg.val_argument }}";		
		{% endifequal %}
				
		
		is_configurable = {% if arg.is_configurable %}true{%else %}false{% endif %};
		
		if( is_configurable){
			arrParams.push({ 'id' : "{{ arg.id }}" , 'nam_argument' : "{{ arg.nam_argument }}",'val_argument' : "{{ arg.val_argument }}", 'dsc_argument' : "{{ arg.dsc_argument }}", 'type_argument' : "{{ arg.type_argument }}"});
		}		
					
	{% endfor %}

	is_configurable = arrParams.length != 0;
	arrFeatures.push(new Feature(featName, {{key}}, featDescription, is_configurable, arrParams));		

{% endfor %}

//Insere todos os elementos do arrFeatures na página HTML.
arrFeatures.forEach(insereFeature);


