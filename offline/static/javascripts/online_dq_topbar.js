// ONLINE_DQ top bar

// Reads out global variables set by python program and sets toolbar icons accordingly
var loading = [false,false];

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
	
    var url = "changeReferenceState?state="+state;
	
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
	
//    
//    $.ajax({
//	    async : true,
//	    type : "GET",
//	    url : url,
//
//	    success : function(json) {
//		if (json.success == false) {
//		    
//		} else {
//		    
//		}
//	    },  
//		
//	    error : function(xhr, ajaxOptions, thrownError) {
//		alert("<2> JSON Error:" + thrownError);
//	    }
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

function set_online_dq_filename_feedback(status_code, el, full_path, visible_name){
    if (status_code == "ROOT_FILE_NOT_FOUND" || status_code == "REFERENCE_FILE_NOT_FOUND"){
	set_status_field(status_code, "danger");
	el.closest('.btn-group').find('btn-text').html('<span id="btn-text">no file</span> <span class="caret"></span>');
    } else {

	if (status_code == "ROOT_FILE_FOUND") loading[0] = true;
	if (status_code == "REFERENCE_FILE_FOUND") loading[1] = true;

	console.log("loading "+loading[0]+" "+loading[1]);
	if (!(loading[0] && loading[1])) {
	    set_status_field(status_code, "info");
	} else {
	    set_status_field("ALL_FILE_LOADED", "success");		    
	    $("#changeReferenceMode").click( function() { change_reference_mode(); } ); 
	}
	el.closest('.btn-group').find('.dropdown-toggle').html('<span id="btn-text">'+visible_name+'</span> <span class="caret"></span>');
    }

    
}

function set_filename(event){
    var el = event.data.element;
    var full_path = event.data.full_path;
    var visible_name = event.data.visible_name;
    var reference_flag = event.data.reference_flag;
    var url = "/online_dq_bp/set_online_dq_filename?filename=";
    if (reference_flag) url = "/online_dq_bp/set_online_dq_reference_filename?filename=";

    console.log("Inside setfilename "+reference_flag);

    $.ajax({
	    async : true,
	    type : "GET",
	    url : url+encodeURIComponent(full_path),

	    success : function(json) {
		console.log("Setting the feedback "+reference_flag);
				    
		set_online_dq_filename_feedback(json.status_code, el, full_path, visible_name);
	    },  

	    error : function(xhr, ajaxOptions, thrownError) {
		alert("JSON Error:" + thrownError);
		set_status_field("JSON Error:" + thrownError, "danger");
	    },
		//		complete : function(){disableNavBar(false);}
	});

}

function build_menu(el, status_code, data, reference_flag){

    if (status_code == "NO_ACCESS") {
	set_status_field("NO access to /hist area", "danger");

    } else if (status_code == "OK") {
	el.empty();
	for(var i = 0; i < data.root_filename.length; i++) {
	    var full_path = data.full_path[i];
	    var visible_name = data.root_filename[i];

	    var html = '<li role="presentation"><a role="menuitem" data-fullpath="' + 
		full_path + 
		'" tabindex="-1" id="' + 
		visible_name.replace(".","_")+reference_flag + 
		'">' + 
		visible_name + 
		'</a></li>';
	    $(el).append(html);



	    $("#"+visible_name.replace(".","_")+reference_flag).on("click", {
		    "element": $(el),
		    "full_path": full_path,
		    "visible_name": visible_name, 
		    "reference_flag": reference_flag}, 
		function( event ) {
		    console.log("Just click "+reference_flag);

		    set_filename(event);
		}
		);
	}
    }
    
}

function init_selector_for_online_dq(el, reference_flag){

    $.ajax({
	   async : true, 
	   type : "GET",
	   url : "get_online_dq_filename",
	   success : function(json){
		console.log("I'll build the menu "+reference_flag);
		build_menu(el, json.status_code, json.data, reference_flag);
	   },
	   error : function(xhr, ajaxOptions, thrownError) {
	       alert("<reconumber> JSON Error:" + thrownError);
	       set_status_field("JSON Error:" + thrownError, "danger");
	   }
	});
}

////////////////////////////////////////////
//jQuery part
////////////////////////////////////////////

$(function() {
	

	init_status_indicator();
	init_reference_state_button();
	el =  $("#filename_online_dq_DropdownMenu");
	init_selector_for_online_dq(el,false);
	ref_el = $("#reference_online_dq_DropdownMenu");
	init_selector_for_online_dq(ref_el, true);


});
