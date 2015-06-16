////////////////////////////////////////////
//Histogram part
////////////////////////////////////////////
function saveAllHistograms()
{
	var elm = $('#histoContainer').find("svg").each( function() 
	{
		var name = $(this).parent().parent().find(".histoTitle").text() + ".png";
		saveSvgAsPng($(this)[0], name);
	}
	);
	
}

////////////////////////////////////////////
//Toolbar part
////////////////////////////////////////////

//reads out global variables set by python program and sets toolbar icons accordingly
function initStatusIndicator()
{
	if(runNmbr == 0 || runNmbr == "")
	{
		setStatusField("No runNmbr provided!", "warning");
	} else if(recoVersionFullPath == "")
	{
		setStatusField("No recoVersion provided!", "warning");
	}
}

function setRunNumbrVisualFeedback(StatusCode, data)
{
	if (StatusCode == "NO_RECOS_FOUND_FOR_RUN_NMBR")
	{
		setStatusField("No RecoVersions found for this runNmbr!", "danger");
		$("#recoVersionDropdownButtonText").text("???");
	}
	else if (StatusCode == "RUN_NMBR_OK")
	{
		$("#recoVersionDropdownMenu").empty();
	
		for(var i = 0; i < data.listOfRecos.length; i++)
		{
			var fullPath = data.listOfRecos[i][0];
			var visibleName = data.listOfRecos[i][1];
			var html = '<li role="presentation"><a role="menuitem" data-fullpath="' + fullPath + '" tabindex="-1" href="#" id="' + visibleName + '">' + visibleName + '</a></li>';
			$("#recoVersionDropdownMenu").append(html);
		
			$("#"+visibleName).on( "click", 
				{
					"fullpath": fullPath,
					"visibleName": visibleName
				}, 
				function( event ) {
					setRecoVersion(event);
				}
			);
		}
	
		//this means, that the previous recoVersion is not available for the current runNmbr
		if(data.selectedRecoVersion == null || data.selectedRecoVersion == "")
		{
			setStatusField("Please choose recoVersion.", "warning");
			$("#recoVersionDropdownButtonText").text("Please select.");
		}
		//activate previous recoVersion.
		//baco
		else{
		    var event = {data: {fullpath: recoVersionFullPath, visibleName: recoVersionVisiblePart} };
		    setRecoVersion(event);

		}		
	
	}
}


//just does the ajax call
function setRunNmbr()
{
	$("#runNmbrTextfieldIndicatorContainer").addClass("hidden");
	var nmbr = $("#runNmbrTextfield").val();
	disableNavBar(true);
	
	if(nmbr != "0")
	{
		setStatusField("Please wait...", "info");
		$.ajax({
			async : true,
			type : "GET",
			url : "setRunNmbr.json?runNmbr="+nmbr,
		
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
		url : "setRecoVersion.json?recoVersion="+encodeURIComponent(fullPath),

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
	
	var url = "changeReferenceState.json?state="+state
	
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


////////////////////////////////////////////
//left side menu part
////////////////////////////////////////////


function checkDBConnection()
{
	$.ajax({
		async : true,
		type : "GET",
		url : "checkDBConnection.json",
		dataType : "json",    

		success : function( data, textStatus, jqXHR ) {
			$("#connectionStatus").css("display", "block");
			if (data.message == 'Could not connect to DB.')
			{
			    	$("#connectionStatusIcon").removeClass("glyphicon-ok");
				$("#connectionStatusIcon").addClass("glyphicon-warning-sign");
				$("#connectionStatus").removeClass("alert alert-success");
				$("#connectionStatus").addClass("alert alert-danger");
				
				$("#connectionStatusText").text("Can't reach DB.");
			}
			else
			{
				$("#connectionStatusIcon").addClass("glyphicon-ok");
				$("#connectionStatusIcon").removeClass("glyphicon-warning-sign");
				$("#connectionStatus").addClass("alert alert-success");
				$("#connectionStatus").removeClass("alert alert-danger");
				
				$("#connectionStatusText").text("DB Connection established.");
			}
		},    

		error : function( jqXHR, textStatus, errorThrown ) {
			$("#connectionStatus").css("display", "block");
			$("#connectionStatus").removeClass("alert alert-success");
			$("#connectionStatus").addClass("alert alert-danger");
			
		    	$("#connectionStatusIcon").removeClass("glyphicon-ok");
			$("#connectionStatusIcon").addClass("glyphicon-warning-sign");
			
			$("#connectionStatusText").text("Can't reach Server.");
		}
	    })
}


////////////////////////////////////////////
//menu tree part
////////////////////////////////////////////

//Parameter "enforceReadFromDBFlag" is set to true, when user manually updates tree
//otherwise, data ist read from file
//Parameter "allNodesStandardState" is considered, when reading from DB. When
// allNodesStandardState == "opened" all nodes are opened
// allNodesStandardState == "closed" all nodes are closed
function treeAjaxCall(enforceReadFromDBFlag, allNodesStandardState, filterFlag, filter)
{
	//if both or any of the both flags is true => read from db
	readFromDB = enforceReadFromDBFlag || pageNormallyReadFromDBFlag
	$.ajax({
		async : true,
		type : "GET",
		url : "tree.json",
		dataType : "json",   
		data: { loadFromDBFlag: readFromDB, allNodesStandardState: allNodesStandardState, filterFlag: filterFlag, filter: filter}, 

		success : function(json) {
		    createJSTrees(json);
		    $("#loading").css("display", "none");
		},    

		error : function(xhr, ajaxOptions, thrownError) {
		    alert("JSON Error:" + thrownError);
		}
	    });
}


function createJSTrees(jsonData) {
    	$("#menuTree").jstree(
	{ 
		'core' : 
		{
		    'data' : jsonData
		}
	}

	);
	
	function selectNode(e, data)
	{
		if (data.node.id.indexOf("//F//") != 0)
      		{
      			$("#connectionStatus").css("display", "none");
      			window.location = "Histo?path="+encodeURIComponent(data.node.id);
      		}
	}
	
	function openNode(e, data)
	{
		
		//Folder Id start not with //F//, so we have a folder
      		if (data.node.id.indexOf("//F//") == 0)
      		{
      			var d = document.getElementById(data.node.id);
      			
      			var object = $(d).children("a").children("i");

      			object.addClass("glyphicon");
      			if(object.hasClass("glyphicon-folder-close"))
      			{
      				object.removeClass("glyphicon-folder-close");
      			}
      			object.addClass("glyphicon-folder-open");
      			
      			//Create ajax call to save tree state
      			$.ajax({
				url: 'menuTreeOpenOrCloseFolder',
				type: 'GET',
				data: { id: data.node.id, action: "open"} ,
				contentType: 'application/json; charset=utf-8',
				success : function(json) {
				},    

				error : function(xhr, ajaxOptions, thrownError) {
				    alert("JSON Error:" + thrownError);
				}
		
			}); 
      		}
	}
	
	function closeNode(e, data)
	{
		//Folder Id start not with //F//, so we have a folder
      		if (data.node.id.indexOf("//F//") == 0)
      		{
      			var d = document.getElementById(data.node.id);
      			
      			var object = $(d).children("a").children("i");

      			object.addClass("glyphicon");
      			if(object.hasClass("glyphicon-folder-open"))
      			{
      				object.removeClass("glyphicon-folder-open");
      			}
      			object.addClass("glyphicon-folder-close");
      			
      			//Create ajax call to save tree state
      			$.ajax({
				url: 'menuTreeOpenOrCloseFolder',
				type: 'GET',
				data: { id: data.node.id, action: "close"} ,
				contentType: 'application/json; charset=utf-8',
				success : function(json) {
				},    

				error : function(xhr, ajaxOptions, thrownError) {
				    alert("JSON Error:" + thrownError);
				}
		
			});
      		}
	}
	
	function reloadTree(event, data)
	{
		$("#menuTree").jstree("destroy");
		$("#loading").css("display", "block");
		treeAjaxCall(true, "closed", false, "");
	}
	
	function openAllTree()
	{
		$("#menuTree").jstree("destroy");
		$("#loading").css("display", "block");
		treeAjaxCall(true, "opened", false, "");
	}
	
	function closeAllTree()
	{
		$("#menuTree").jstree("destroy");
		$("#loading").css("display", "block");
		treeAjaxCall(true, "closed", false, "");
	}
	
	function addFilter()
	{
		var filter = $("#filterTextfield").val();
		$("#menuTree").jstree("destroy");
		$("#loading").css("display", "block");
		treeAjaxCall(true, "opened", true, filter);
	}
	
	function removeFilter()
	{
		$("#filterTextfield").val("");
		$("#menuTree").jstree("destroy");
		$("#loading").css("display", "block");
		treeAjaxCall(true, "closed", false, "");
	}
	
	$("#menuTree").bind("open_node.jstree",function(event,data){openNode(event, data)});
	$("#menuTree").bind("close_node.jstree",function(event,data){closeNode(event, data)});
	$("#menuTree").bind("select_node.jstree",function(event,data){selectNode(event, data)});
	
	$("#menuTree").bind("loaded.jstree", function (event, data) {
		$("#reloadTreeButton").click( function() { reloadTree() } );
		$("#openAllTreeButton").click( function() { openAllTree() } );
		$("#closeAllTreeButton").click( function() { closeAllTree() } );
		$("#addFilterButton").click( function() { addFilter() } );
		$("#removeFilterButton").click( function() { removeFilter() } );
	})
} 

////////////////////////////////////////////
//jQuery part
////////////////////////////////////////////

$(function() {
	initReferenceStateButton();
	
	initStatusIndicator();
	initRunNmbrIcon();
	initRecoVersion(recoVersionVisiblePart);
	$("#setRunNmbrButton").click( function() { setRunNmbr() } ); 
	$("#changeReferenceMode").click( function() { changeReferenceMode(); } ); 
	$("#decreaseRunNmbrButton").click( function() { decreaseRunNmbr(); } ); 
	$("#increaseRunNmbrButton").click( function() { increaseRunNmbr(); } ); 
	
	

	treeAjaxCall(false, "closed", false, "");
	
	checkDBConnection();
	//check DB Connection every minute
	window.setInterval(checkDBConnection, 1000*60*1);
});
