// ONLINE_DQ top bar

// Reads out global variables set by python program and sets toolbar icons accordingly
var loading = [false,false];

// Disable buttons while loading
function disable_nav_bar(disabled){
  var buttons = $('.btn-default').each(function(){
	  if (disabled){
		$(this).addClass('disabled');
	  }		
	  else{
		$(this).removeClass('disabled');
	  }
	});
  
}


function init_status_indicator() {
    	
  if(filename == "") {
    set_status_field("Filename not provided!", "warning");
  } else if(reference_filename == "") {
    set_status_field("Reference Filename not provided!", "warning");
  }

}


function init_reference_state_button() {
    var button = $("#changeReferenceMode");
    var icon = $("#changeReferenceModeIcon");
    var text = $("#changeReferenceModeText");
	
    state = button.data("state");
    
    if(state == "activated"){	
	button.removeClass("btn-danger");
	button.addClass("btn-success");
	
	icon.removeClass("glyphicon-remove");
	icon.addClass("glyphicon-ok");
	
	text.text(" Activated");
    }else{
	button.removeClass("btn-success");
	button.addClass("btn-danger");
	
	icon.removeClass("glyphicon-ok");
	icon.addClass("glyphicon-remove");
	
	text.text(" Deactivated");		
    }
}



function change_reference_mode(){
    var button = $("#changeReferenceMode");
    var icon = $("#changeReferenceModeIcon");
    var text = $("#changeReferenceModeText");
	
    state = button.data("state");
	
    //    var url = "changeReferenceState?state="+state;
	
    //current state deactivated -> change it
    if(state == "deactivated"){
	button.data("state", "activated");
	
	button.removeClass("btn-danger");
	button.addClass("btn-success");
		
	icon.removeClass("glyphicon-remove");
	icon.addClass("glyphicon-ok");
		
	text.text(" Activated");
		
	url = url + "activated";
	
	OfflineApp.redrawHistograms("activated");
    } else {
	button.data("state", "deactivated");
	
	button.removeClass("btn-success");
	button.addClass("btn-danger");
		
	icon.removeClass("glyphicon-ok");
	icon.addClass("glyphicon-remove");
	
	text.text(" Deactivated");
	
	url = url + "deactivated";
	OfflineApp.redrawHistograms("deactivated");				
    }
		  
}




function set_status_field(message, status)
{
    $("#statusIndicatorContainer").removeClass("btn-success");
    $("#statusIndicatorContainer").removeClass("btn-danger");
    $("#statusIndicatorContainer").removeClass("btn-info");
    $("#statusIndicatorContainer").removeClass("btn-warning");
    
    $("#statusIndicatorIcon").removeClass("glyphicon-ok");
    $("#statusIndicatorIcon").removeClass("glyphicon-exclamation-sign");
    $("#statusIndicatorIcon").removeClass("glyphicon-question-sign");
    
    if(status == "warning"){
	$("#statusIndicatorContainer").addClass("btn-warning");
	$("#statusIndicatorIcon").addClass("glyphicon-question-sign");
    }else if(status == "danger"){
	$("#statusIndicatorContainer").addClass("btn-danger");
	$("#statusIndicatorIcon").addClass("glyphicon-exclamation-sign");
    }else if(status == "info"){
	$("#statusIndicatorContainer").addClass("btn-info");
	$("#statusIndicatorIcon").addClass("glyphicon-exclamation-sign");
    }else if(status == "success"){
	$("#statusIndicatorContainer").addClass("btn-success");
	$("#statusIndicatorIcon").addClass("glyphicon-ok");
    }else{
	alert("Unrecognised Status for status field!");
    }
		
    $("#statusIndicatorText").text(message);

}

function set_run_number_visual_feedback(sc, data) {
    if (sc == "ROOT_FILE_NOT_FOUND") {
	set_status_field(sc, "danger");
	$("#changeReferenceMode").click( function() { return false; } ); 
    } else if (sc == "ROOT_AND_REFERENCE_NOT_FOUND") {
	set_status_field(sc, "danger");
	$("#changeReferenceMode").click( function() { return false; } ); 
    } else if (sc == "ROOT_FILE_FOUND_NO_REF") {
	set_status_field(sc, "warning");	
	$("#changeReferenceMode").click( function() { return false; } ); 
    } else if (sc == "ROOT_AND_REFERENCE_FOUND") {
	set_status_field(sc, "success");	
	$("#changeReferenceMode").click( function() { change_reference_mode(); } ); 
    }
}



function set_run_number() {

    $("#runNmbrTextfieldIndicatorContainer").addClass("hidden");
    var number = $("#runNmbrTextfield").val();
    disable_nav_bar(false);
  
    if(number != "0") {
	set_status_field("Please wait...", "info");
	$.ajax({
		async : true,
		type : "GET",
		url : "set_run_number?run_number="+number,
		
		success : function(json) {
		    set_run_number_visual_feedback(json.StatusCode, json.data);
		},  

		error : function(xhr, ajaxOptions, thrownError) {
		    alert("<runnumber> JSON Error:" + thrownError);
		    set_status_field("JSON Error:" + thrownError, "danger");
		    $("#recoVersionDropdownButtonText").text("???");
		},

		complete : function(){disable_nav_bar(false);}
		});
	  
	}
	

}



function init_run_number_icon() {
    if($("#runNmbrTextfield").val() != ""){
	set_run_number();
    }
}

function decrease_run_number() {
    if($("#runNmbrTextfield").val() != ""){
	var val = parseInt($("#runNmbrTextfield").val()) -1;
	$("#runNmbrTextfield").val(val);
	set_run_number();
    }
}

function increase_run_number() {
    if($("#runNmbrTextfield").val() != "") {
	var val = parseInt($("#runNmbrTextfield").val()) +1;
	$("#runNmbrTextfield").val(val);
	set_run_number();
    }
}


////////////////////////////////////////////
//jQuery part
////////////////////////////////////////////

$(function() {	

	init_status_indicator();
	init_reference_state_button();
	init_run_number_icon();
	$("#runNmbrTextfield").keypress(function (e){ 
		if (e.keyCode == 13) { 
		    set_run_number(); 
		    return false;
		} 
	    }); 
	$("#setRunNmbrButton").click( function() { set_run_number(); } ); 
	$("#decreaseRunNmbrButton").click( function() { decrease_run_number(); } ); 
	$("#increaseRunNmbrButton").click( function() { increase_run_number(); } ); 	

});
