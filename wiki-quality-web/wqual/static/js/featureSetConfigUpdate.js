$( function() {
	
	$( "#add-form" ).dialog({
	
	     autoOpen: false,
	     modal: true,
	     width: 400, 
		 height: 'auto',
		 fluid: true, 
		 resizable: false,
	     
	     buttons: {
	        "Save": function() {
	          $( this ).dialog( "close" );
	          let arr_checked = $('input[type=checkbox]:checked');
	          let arrFeaturesNames = new Array();
	         
	          for(let intI=0; intI < arr_checked.length; intI++){
	          	arrFeaturesNames.push(arr_checked[intI].value);
	          }
	         	         
	         let strFeatureSet = "";
	         
	         strFeatureSet = $('#id_nam_feature_set').val();
	         
	         if(arrFeaturesNames.length != 0){
	         	insertFeatures(arrFeaturesNames,strFeatureSet);
	         }
	          
	          HTMLEl_temp_div_add_feature.innerHTML = "";
	        },
	        
	        Cancel: function() {
	          $( this ).dialog( "close" );
	          HTMLEl_temp_div_add_feature.innerHTML = "";
	        }
	      }
	
	});
	
	$( ".ui-dialog-titlebar-close" ).on( "click", function() {
		
		HTMLEl_temp_div_add_feature.innerHTML = "";
	        
	});
	 
	$( "#insert" ).on( "click", function() {
	    
	     $( "#add-form" ).dialog( "open" );
	     let combo = $('#id_language')[0];
	     let textoCombo = combo.options[combo.selectedIndex].text;
	     let lingua = textoCombo.substring(1, 3);
	     let list = $("#featureList");
	     getFeatureList( list[0] ,lingua);
	
	});


	$('#id_nam_feature_set').addClass('form-control');
	$('#id_dsc_feature_set').addClass('form-control');
	
    $.widget( "custom.combobox", {
      _create: function() {
        this.wrapper = $( "<span>" )
          .addClass( "custom-combobox" )
          .insertAfter( this.element );
 
        this.element.hide();
        this._createAutocomplete();
        this._createShowAllButton();
      },
 
      _createAutocomplete: function() {
        var selected = this.element.children( ":selected" ),
          value = selected.val() ? selected.text() : "";
 
        this.input = $( "<input>" )
          .appendTo( this.wrapper )
          .val( value )
          .attr( "title", "" )
          .addClass( "custom-combobox-input ui-widget ui-widget-content ui-state-default ui-corner-left" )
          .autocomplete({
            delay: 0,
            minLength: 0,
            source: $.proxy( this, "_source" )
          })
          .tooltip({
            classes: {
              "ui-tooltip": "ui-state-highlight"
            }
          });
 
        this._on( this.input, {
          autocompleteselect: function( event, ui ) {
            ui.item.option.selected = true;
            this._trigger( "select", event, {
              item: ui.item.option
            });
          },
 
          autocompletechange: "_removeIfInvalid"
        });
      },
 
      _createShowAllButton: function() {
        var input = this.input,
          wasOpen = false;
 
        $( "<a>" )
          .attr( "tabIndex", -1 )
          .attr( "title", "Show All Languages" )
          .tooltip()
          .appendTo( this.wrapper )
          .button({
            icons: {
              primary: "ui-icon-triangle-1-s"
            },
            text: false
          })
          .removeClass( "ui-corner-all" )
          .addClass( "custom-combobox-toggle ui-corner-right" )
          .on( "mousedown", function() {
            wasOpen = input.autocomplete( "widget" ).is( ":visible" );
          })
          .on( "click", function() {
            input.trigger( "focus" );
 
            // Close if already visible
            if ( wasOpen ) {
              return;
            }
 
            // Pass empty string as value to search for, displaying all results
            input.autocomplete( "search", "" );
          });
      },
 
      _source: function( request, response ) {
        var matcher = new RegExp( $.ui.autocomplete.escapeRegex(request.term), "i" );
        response( this.element.children( "option" ).map(function() {
          var text = $( this ).text();
          if ( this.value && ( !request.term || matcher.test(text) ) )
            return {
              label: text,
              value: text,
              option: this
            };
        }) );
      },
 
      _removeIfInvalid: function( event, ui ) {
 
        // Selected an item, nothing to do
        if ( ui.item ) {
          return;
        }
 
        // Search for a match (case-insensitive)
        var value = this.input.val(),
          valueLowerCase = value.toLowerCase(),
          valid = false;
        this.element.children( "option" ).each(function() {
          if ( $( this ).text().toLowerCase() === valueLowerCase ) {
            this.selected = valid = true;
            return false;
          }
        });
 
        // Found a match, nothing to do
        if ( valid ) {
          return;
        }
 
        // Remove invalid value
        this.input
          .val( "" )
          .attr( "title", value + " didn't match any item" )
          .tooltip( "open" );
        this.element.val( "" );
        this._delay(function() {
          this.input.tooltip( "close" ).attr( "title", "" );
        }, 2500 );
        this.input.autocomplete( "instance" ).term = "";
      },
 
      _destroy: function() {
        this.wrapper.remove();
        this.element.show();
      }
    });
 
    $( "#id_language" ).combobox();
        
 } );
 
