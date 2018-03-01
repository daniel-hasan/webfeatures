$(document).ready(function() {
	$("#modal").dialog({ autoOpen: false });
		$("#informations-modal").click(function() {
			$("#modal").dialog("open");
		});
	$("#feature_set_list").dialog({
	      autoOpen: false,
	      height: 400,
	      width: 700,
	      modal: true,
	});
	$("#show_featureset").click( function() {
						$("#feature_set_list").dialog("open");
						return false;
					}
					);

});
