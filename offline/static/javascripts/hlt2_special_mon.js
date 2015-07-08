// HLT2 file selector

function build_menu(el, status_code, data){
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
      
	    //		$("#"+visibleName).on("click", {
	    //			"fullpath": fullPath,
	    //			    "visibleName": visibleName }, 
	    //		    function( event ) {
	    //			setRecoVersion(event);
	    //		    }
	    //		    );

	    

	}
    }
}

function init_selector_for_hlt2(el){
    $.ajax({
	   async : true, 
	   type : "GET",
	   url : "get_hlt2_filename",
	   success : function(json){
	       build_menu(el, json.status_code, json.data);
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

	init_selector_for_hlt2($("#filename_HLT2_DropdownMenu"));
	init_selector_for_hlt2($("#reference_filename_HLT2_DropdownMenu"));

});
