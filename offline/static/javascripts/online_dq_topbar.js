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
    console.log("init reference >> ",state);

    if(state == "activated"){	
	button.removeClass("btn-danger");
	icon.removeClass("glyphicon-remove");

	setTimeout(function () {
		button.addClass("btn-success");	
		icon.addClass("glyphicon-ok");
		text.text(" Activated");
	    },
	    10);	
    }else if(state == "deactivated"){
	button.removeClass("btn-success");
	
	icon.removeClass("glyphicon-ok");
	
	setTimeout(function () {
		button.addClass("btn-danger");
		icon.addClass("glyphicon-remove");
		text.text(" Deactivated");		
	    },
	    10);	

    }else{
	button.removeClass("btn-success");	
	icon.removeClass("glyphicon-ok");
	button.addClass("btn-danger");
	button.data("state","deactivated");
	icon.addClass("glyphicon-remove");
	text.text(" Deactivated");		
	setTimeout(function () {
		console.log("protection reference >> ",state);
	    },
	    10);	

    }
}


function change_reference_mode(){
    var button = $("#changeReferenceMode");
    var icon = $("#changeReferenceModeIcon");
    var text = $("#changeReferenceModeText");
	
    state = button.data("state");
    console.log("change reference from:",state);
	
    var url = "change_reference_state?state="+state;
	
    //current state deactivated -> change it
    if(state == "deactivated"){
	
	button.removeClass("btn-danger");
		
	icon.removeClass("glyphicon-remove");


	setTimeout(function () {
		button.data("state", "activated");
		button.addClass("btn-success");
		icon.addClass("glyphicon-ok");
		text.text(" Activated");
		url = url + "activated";
		console.log("to>>>",state);
		OfflineApp.redrawHistograms();
	    },
	    10);	

		

    } else {
	
	button.removeClass("btn-success");		
	icon.removeClass("glyphicon-ok");

	setTimeout(function () {
		button.data("state", "deactivated");
		button.addClass("btn-danger");
		icon.addClass("glyphicon-remove");
		text.text(" Deactivated");
		url = url + "deactivated";
		console.log(state);
		OfflineApp.redrawHistograms();				
	    },
	    10);	

	
    }
    
//    $.ajax({
//	    async : true,
//	    type : "GET",
//	    url : url,
//	    success : function(json) {
//		if (json.success == false){
//		    
//		} else {
//		    
//		}
//	    },  
//
//	    error : function(xhr, ajaxOptions, thrownError) {
//		alert("<2> JSON Error:" + thrownError);
//	    },
//	    complete: function(){disable_nav_bar(false);}
//  	});

	  
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
	set_status_field("", "danger");
	//	$("#changeReferenceMode").click( function() { return false; } ); 
    } else if (sc == "ROOT_AND_REFERENCE_NOT_FOUND") {
	set_status_field("", "danger");
	//	$("#changeReferenceMode").click( function() { return false; } ); 
    } else if (sc == "ROOT_FILE_FOUND_NO_REF") {
	set_status_field("", "warning");	
	//	$("#changeReferenceMode").click( function() { return false; } ); 
    } else if (sc == "ROOT_AND_REFERENCE_FOUND") {
	set_status_field("", "success");	
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
		url : "set_run_number?runnumber="+number,
		
		success : function(json) {
		    set_run_number_visual_feedback(json.StatusCode, json.data);
		},  

		error : function(xhr, ajaxOptions, thrownError) {
		    alert("<runnumber> JSON Error:" + thrownError);
		    set_status_field("JSON Error:" + thrownError, "danger");
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
	var runnumber = parseInt($("#runNmbrTextfield").val());
	$.ajax({
		async : true,
		type : "GET",
		url : "get_previous_runnumber?runnumber="+runnumber,
		
		success : function(json) {
		    $("#runNmbrTextfield").val(json['data']['runnumber']);
		    set_run_number();

		},  

		error : function(xhr, ajaxOptions, thrownError) {
		    alert("<runnumber> JSON Error:" + thrownError);
		    set_status_field("JSON Error:" + thrownError, "danger");
		},
		complete : function(){disable_nav_bar(false);}
	    });
	  
    }

    
}

function increase_run_number() {
    if($("#runNmbrTextfield").val() != ""){
	var runnumber = parseInt($("#runNmbrTextfield").val());
	$.ajax({
		async : true,
		type : "GET",
		url : "get_next_runnumber?runnumber="+runnumber,
		
		success : function(json) {
		    $("#runNmbrTextfield").val(json['data']['runnumber']);
		    set_run_number();			
		},  

		error : function(xhr, ajaxOptions, thrownError) {
		    alert("<runnumber> JSON Error:" + thrownError);
		    set_status_field("JSON Error:" + thrownError, "danger");
		},
		complete : function(){disable_nav_bar(false);}
	    });
	  
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
	$("#changeReferenceMode").click( function() { change_reference_mode(); } ); 
	$("#setRunNmbrButton").click( function() { set_run_number(); } ); 
	$("#decreaseRunNmbrButton").click( function() { decrease_run_number(); } ); 
	$("#increaseRunNmbrButton").click( function() { increase_run_number(); } ); 	

});
