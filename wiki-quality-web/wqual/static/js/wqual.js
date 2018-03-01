$( function() {
	var dialog;
		  
	    dialog = $( "#add-form" ).dialog({
	      autoOpen: false,
	      height: 200,
	      width: 500,
	      modal: true,
	    });
	 
	    $( "#insert" ).button().on( "click", function() {
	      dialog.dialog( "open" );
	    });
	
	    $( "#Cancel" ).button().on( "click", function() {
	      dialog.dialog( "close" );
	    });
} );

function itemSelecionado(strIdItem){
	alert(strIdItem);

}
