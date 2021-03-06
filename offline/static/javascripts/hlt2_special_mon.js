// HLT2 top bar

// Reads out global variables set by python program and sets toolbar icons accordingly
function initStatusIndicator() {

  if(filename == "") {
    setStatusField("Filename not provided!", "warning");
  } else if(reference_filename == "") {
    setStatusField("Reference Filename not provided!", "warning");
  }

}


function setStatusField(message, status)
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

function setfilename(event){
    var full_path = event.data.full_path;
    var visible_name = event.data.visible_name;
    var reference_flag = event.data.reference_flag;
    var url = "set_hlt2_filename?filename=";
    if (reference_flag) url = "set_hlt2_reference_filename?filename=";

    $.ajax({
	    async : true,
	    type : "GET",
	    url : url+encodeURIComponent(fullPath),

	    success : function(json) {
		set_hlt2_filename_feedback(json.status_code, full_path, visible_name);
	    },  

	    error : function(xhr, ajaxOptions, thrownError) {
		alert("JSON Error:" + thrownError);
		setStatusField("JSON Error:" + thrownError, "danger");
	    }//,
		//		complete : function(){disableNavBar(false);}
	});

}

function build_menu(el, status_code, data, reference_flag){
    if (status_code == "NO_ACCESS") {
	console.log("NO access to /hist area");
    } else if (status_code == "OK") {
	$(el).empty();
	for(var i = 0; i < data.root_filename.length; i++) {
	    var full_path = data.full_path[i];
	    var visible_name = data.root_filename[i];
	    var html = '<li role="presentation"><a role="menuitem" data-fullpath="' + 
		full_path + 
		'" tabindex="-1" href="#" id="' + 
		visible_name + 
		'">' + 
		visible_name + 
		'</a></li>';
	    $(el).append(html);
      
	    $("#"+visible_name).on("click", {
		    "fullpath": full_path,
		    "visible_name": visible_name, 
		    "reference_flag": reference_flag}, 
		function( event ) {
		    setFilename(event);
		});

	}
    }
}

function init_selector_for_hlt2(el, reference_flag){
    $.ajax({
	   async : true, 
	   type : "GET",
	   url : "get_hlt2_filename",
	   success : function(json){
		build_menu(el, json.status_code, json.data, reference_flag);
	   },
	   error : function(xhr, ajaxOptions, thrownError) {
	       alert("<reconumber> JSON Error:" + thrownError);
	       //	       setStatusField("JSON Error:" + thrownError, "danger");
	   }
	});
}
////////////////////////////////////////////
//jQuery part
////////////////////////////////////////////

$(function() {

	initStatusIndicator();
	init_selector_for_hlt2($("#filename_HLT2_DropdownMenu", false));
	init_selector_for_hlt2($("#reference_filename_HLT2_DropdownMenu", true));

});
