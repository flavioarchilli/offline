// Offline Toolbar

// Reads out global variables set by python program and sets toolbar icons accordingly
function initStatusIndicator() {

  if(runNmbr == 0 || runNmbr == "") {
    setStatusField("No runNmbr provided!", "warning");
  } else if(recoVersionFullPath == "") {
    setStatusField("No recoVersion provided!", "warning");
  }

}


// Set the Run Number and show if it is available 

function setRunNumbrVisualFeedback(StatusCode, data) {
  if (StatusCode == "NO_RECOS_FOUND_FOR_RUN_NMBR") {
    setStatusField("No RecoVersions found for this runNmbr!", "danger");
    $("#recoVersionDropdownButtonText").text("???");
  } else if (StatusCode == "RUN_NMBR_OK") {
    $("#recoVersionDropdownMenu").empty();
    
    for(var i = 0; i < data.listOfRecos.length; i++) {
      var fullPath = data.listOfRecos[i][0];
      var visibleName = data.listOfRecos[i][1];
      var html = '<li role="presentation"><a role="menuitem" data-fullpath="' + 
                 fullPath + 
	         '" tabindex="-1" href="#" id="' + 
                 visibleName + 
                 '">' + 
                 visibleName + 
                 '</a></li>';
      $("#recoVersionDropdownMenu").append(html);
      
      $("#"+visibleName).on("click", {
	      "fullpath": fullPath,
	      "visibleName": visibleName }, 
	  function( event ) {
	      setRecoVersion(event);
	  }
	  );
    }
    
    //this means, that the previous recoVersion is not available for the current runNmbr
    if(data.selectedRecoVersion == null || data.selectedRecoVersion == "") {
      setStatusField("Please choose recoVersion.", "warning");
      $("#recoVersionDropdownButtonText").text("Please select.");
    } else {
      //activate previous recoVersion.
      //baco
     
      var event = {data: {fullpath: recoVersionFullPath, visibleName: recoVersionVisiblePart} };
      setRecoVersion(event);
      
    }         
  }
}

//just does the ajax call
function setRunNmbr() {
  $("#runNmbrTextfieldIndicatorContainer").addClass("hidden");
  var nmbr = $("#runNmbrTextfield").val();
  disableNavBar(false);
  
  if(nmbr != "0")
	{
	  setStatusField("Please wait...", "info");
	  $.ajax({
		  async : true,
			type : "GET",
			url : "setRunNumber?runNmbr="+nmbr,
		
			success : function(json) {
			setRunNumbrVisualFeedback(json.StatusCode, json.data)
			  },  

			error : function(xhr, ajaxOptions, thrownError) {
			alert("<runnumber> JSON Error:" + thrownError);
			setStatusField("JSON Error:" + thrownError, "danger");
			$("#recoVersionDropdownButtonText").text("???");
		  },

			complete : function(){disableNavBar(false);}
		});
	  
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
	
	if(status == "warning")
	{
		$("#statusIndicatorContainer").addClass("btn-warning");
		$("#statusIndicatorIcon").addClass("glyphicon-question-sign");
	}
	else if(status == "danger")
	{
		$("#statusIndicatorContainer").addClass("btn-danger");
		$("#statusIndicatorIcon").addClass("glyphicon-exclamation-sign");
	}
	else if(status == "info")
	{
		$("#statusIndicatorContainer").addClass("btn-info");
		$("#statusIndicatorIcon").addClass("glyphicon-exclamation-sign");
	}
	else if(status == "success")
	{
		$("#statusIndicatorContainer").addClass("btn-success");
		$("#statusIndicatorIcon").addClass("glyphicon-ok");
	}
	else
	{
		alert("Unrecognised Status for status field!");
	}
		
	$("#statusIndicatorText").text(message);
}

function setRecoVersionVisualFeedback(StatusCode, fullPath, visibleName)
{
	if (StatusCode == "ROOT_FILE_NOT_FOUND")
	{
		setStatusField("Root file not found!", "danger");
		$("#recoVersionDropdownButtonText").text("???");
	}
	else if (StatusCode == "REFERENCE_FILE_NOT_FOUND")
	{
		setStatusField("Reference file not found!", "danger");
		$("#recoVersionDropdownButtonText").text("???");
	} 
	else if (StatusCode == "ROOT_AND_REFERENCE_FOUND")
	{
		setStatusField("Root file loaded.", "success");
		$("#recoVersionDropdownButtonText").text(visibleName);
	}
	else
	{
		alert("Undefined status code:"+StatusCode);
		setStatusField("Undefined status code:"+StatusCode, "danger");
		$("#recoVersionDropdownButtonText").text("???");
	}
}

//
function setRecoVersion(event)
{
	var fullPath = event.data.fullpath;
	var visibleName = event.data.visibleName;
	
	
	setStatusField("Please wait...", "info");
	$("#recoVersionDropdownButtonText").text("Please wait");
	disableNavBar(true);
	
	$.ajax({
		async : true,
		type : "GET",
		url : "setRecoVersion?recoVersion="+encodeURIComponent(fullPath),

		success : function(json) {
			setRecoVersionVisualFeedback(json.StatusCode, fullPath, visibleName);
		},  

		error : function(xhr, ajaxOptions, thrownError) {
		  alert("<reconumber> JSON Error:" + thrownError);
		  setStatusField("JSON Error:" + thrownError, "danger");
		  $("#recoVersionDropdownButtonText").text("???");
		},
		complete : function(){disableNavBar(false);}
	  });
	

}

function initRecoVersion(visibleName)
{
	if(recoVersionVisiblePart != "")
	{
		$("#recoVersionDropdownButtonText").text(visibleName);
	}
}

function initReferenceStateButton()
{
	var button = $("#changeReferenceMode")
	var icon = $("#changeReferenceModeIcon")
	var text = $("#changeReferenceModeText")
	
	state = button.data("state");
	
	if(state == "activated")
	{	
		button.removeClass("btn-danger");
		button.addClass("btn-success");
		
		icon.removeClass("glyphicon-remove");
		icon.addClass("glyphicon-ok");
		
		text.text(" Activated");
	}
	else
	{
		button.removeClass("btn-success");
		button.addClass("btn-danger");
		
		icon.removeClass("glyphicon-ok");
		icon.addClass("glyphicon-remove");
		
		text.text(" Deactivated");		
	}
}

function initRunNmbrIcon()
{
	if($("#runNmbrTextfield").val() != "")
	{
		setRunNmbr();
	}
}

function decreaseRunNmbr()
{
	if($("#runNmbrTextfield").val() != "")
	{
		var val = parseInt($("#runNmbrTextfield").val()) -1;
		$("#runNmbrTextfield").val(val);
		setRunNmbr();
	}
}

function increaseRunNmbr()
{
	if($("#runNmbrTextfield").val() != "")
	{
		var val = parseInt($("#runNmbrTextfield").val()) +1;
		$("#runNmbrTextfield").val(val);
		setRunNmbr();
	}
}

function changeReferenceMode()
{
	var button = $("#changeReferenceMode")
	var icon = $("#changeReferenceModeIcon")
	var text = $("#changeReferenceModeText")
	
	state = button.data("state");
	
	var url = "changeReferenceState?state="+state
	
	//current state deactivated -> change it
	if(state == "deactivated")
	{
		button.data("state", "activated");
		
		button.removeClass("btn-danger");
		button.addClass("btn-success");
		
		icon.removeClass("glyphicon-remove");
		icon.addClass("glyphicon-ok");
		
		text.text(" Activated");
		
		url = url + "activated"
		
		WebMonitor.redrawHistograms("activated");
	}
	else
	{
		button.data("state", "deactivated");
		
		button.removeClass("btn-success");
		button.addClass("btn-danger");
		
		icon.removeClass("glyphicon-ok");
		icon.addClass("glyphicon-remove");
		
		text.text(" Deactivated");
		
		url = url + "deactivated"
		
		WebMonitor.redrawHistograms("deactivated");				
	}
	
	disableNavBar(true);

	$.ajax({
		async : true,
		type : "GET",
		url : url,

		success : function(json) {
			if (json.success == false)
			{
		
			}
			else
			{
		
			}
		},  

		error : function(xhr, ajaxOptions, thrownError) {
		  alert("<2> JSON Error:" + thrownError);
		},
		  complete: function(){disableNavBar(false);}
  	});
	  
}

// Disable buttons while loading
function disableNavBar(isDisabled){
  var buttons = $('.btn-default').each(function(){
	  if (isDisabled){
		$(this).addClass('disabled');
	  }		
	  else{
		$(this).removeClass('disabled');
	  }
	});
  
}


$(function() {
  
  initReferenceStateButton();
  initStatusIndicator();
  initRunNmbrIcon();
  initRecoVersion(recoVersionVisiblePart);

  $("#setRunNmbrButton").click( function() { setRunNmbr() } ); 
  $("#changeReferenceMode").click( function() { changeReferenceMode(); } ); 
  $("#decreaseRunNmbrButton").click( function() { decreaseRunNmbr(); } ); 
  $("#increaseRunNmbrButton").click( function() { increaseRunNmbr(); } ); 
         
});
