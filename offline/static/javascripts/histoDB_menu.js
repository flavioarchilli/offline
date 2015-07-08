function checkDBConnection()
{
	$.ajax({
		async : true,
		type : "GET",
		url : "/histogramDB_tree_menu/checkDBConnection",
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


// Menu Tree
// Parameter "enforceReadFromDBFlag" is set to true, when user manually updates tree
// otherwise, data ist read from file
// Parameter "allNodesStandardState" is considered, when reading from DB. When
// allNodesStandardState == "opened" all nodes are opened
// allNodesStandardState == "closed" all nodes are closed
function treeAjaxCall(enforceReadFromDBFlag, allNodesStandardState, filterFlag, filter)
{
	//if both or any of the both flags is true => read from db
        console.log("I'm here in treeAjaxCall")
	readFromDB = enforceReadFromDBFlag || pageNormallyReadFromDBFlag
	$.ajax({
		async : true,
		type : "GET",
		url : "/histogramDB_tree_menu/menutree",
		dataType : "json",   
		data: { 
		    loadFromDBFlag: readFromDB, 
		    allNodesStandardState: allNodesStandardState, 
		    filterFlag: filterFlag, 
		    filter: filter}, 
		success : function(json) {
		  console.log("I'll create a JStree");
		  createJSTrees(json);
		  $("#loading").css("display", "none");
		},  
		error : function(xhr, ajaxOptions, thrownError) {
		  console.log("Error on menutree");
		  alert("JSON Error:" + thrownError);
		}
	  });
}


function createJSTrees(jsonData) {
    console.log("I'm inside createJSTrees");
    
    console.log(jsonData);
    $("#menuTree").jstree({
	    "core" : {
		"animation" : 1,
		"data" : jsonData
	    }
     });
	
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
			url: '/histogramDB_tree_menu/menuTreeOpenOrCloseFolder',
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
			url: '/histogramDB_tree_menu/menuTreeOpenOrCloseFolder',
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
    
  treeAjaxCall(false, "closed", false, "");       
  checkDBConnection();
  
  //check DB Connection every minute
  window.setInterval(checkDBConnection, 1000*60*1);       

});
