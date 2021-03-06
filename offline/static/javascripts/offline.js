// This structure is similar to that used by WebMonitor.js.
// You have access to both the WebMonitor object and activePage (if the page
// is being served by the catchall.serve_page route), which you can use to
// determine what page you're own, and hence what things need doing.
var OfflineApp = (function(window, undefined) {
  'use strict';

  // Display msg inside log, styled as a red error box
  // Accepts:
  //   container: jQuery element to insert msg into
  //   msg: HTML message to display inside container
  var displayFailure = function(container, msg) {
      console.log(msg);
  };

  var constants = {
    s_Area: "AREA",
    s_Entries: "ENTR",
    s_NoReference: "NOREF",
    s_NoNormalization: "NONE"
  };


  var localCache = {
      listOfHistogramData: [],
  };


  var empty_data = [{ xlow: 0,
		     xhigh: 0.1,
		     y: 0,
		     yerr: 0
  }];


  // Draw a histogram in the `container` using `options`.
  // Accepts:
  //   container: A jQuery object in which to draw the histogram
  //     If the jQuery object references multiple DOM nodes, the first is used
  //   data: An array of data points formatted for d3.chart.histogram
  //   options: Object of options passed to the plotting library
  //     Any present options override those in WebMonitor.settings.histogramDefaults
  // Returns:
  //   undefined
  var drawHistogram = function(container, data, referenceData, options, refOptions, histFail, refFail) {

    var opt = $.extend(true, {}, WebMonitor.settings.histogramDefaults, options);
    var refopt = $.extend(true, {}, WebMonitor.settings.histogramDefaults, refOptions);

//    console.log("opt.title = ",opt.title);
//    var optionsName = 'OPTIONS_FOR_'+opt.title;
//    var histoOptions = document.getElementById(optionsName);
//    console.log("histoOptions = ",histoOptions);

//    var xLabel ="", yLabel="";
//    var histoLabel = histoOptions.getAttribute('data-lab-histo');
//    var histoCx = histoOptions.getAttribute('data-center-x');
//    var histoCy = histoOptions.getAttribute('data-center-y');
//    var histoSx = histoOptions.getAttribute('data-size-x');
//    var histoSy = histoOptions.getAttribute('data-size-y');
//    if (histoOptions!=null) {
//	xLabel = histoOptions.getAttribute('data-lab-x');
//	yLabel = histoOptions.getAttribute('data-lab-y');
//	histoLabel = histoOptions.getAttribute('data-lab-histo');	
//    }


    var histoLabel = opt["title"],
    histoCx = opt["center-x"],
    histoCy = opt["center-y"],
    histoSx = opt["size-x"],
    histoSy = opt["size-y"],
    xLabel = opt["xAxis"],
    yLabel = opt["yAxis"];    

    var cx = opt["canvassize"][0] * parseFloat(histoCx);
    var cy = opt["canvassize"][1] * parseFloat(histoCy) + 150;
    var sx = opt["canvassize"][0] * (parseFloat(histoSx) - parseFloat(histoCx));
    var sy = opt["canvassize"][1] * (parseFloat(histoSy) - parseFloat(histoCy));

    console.log("Sx",sx);
    console.log("Sy",sy);
    
    container.get()[0].setAttribute("style",
	    "position : absolute;"+ 
		"top : "+cy+"px;"+
		"left : "+cx+"px;"+
		"width : "+sx+"px;"+
		"height : "+sy+"px;"
    );
//    console.log(container.get()[0]);

    var chart = d3.select(container.get()[0]).append('svg')
    .attr('width', container.width())
    .attr('height', container.height())
    .chart('AxesChart')
    .xAxisLabel(xLabel)
    .yAxisLabel(yLabel);

    var myWidth = container.width();
    var myHeight = container.height();

    console.log("myWidth",myWidth);
    console.log("myHeight",myHeight);
    chart.addOrnament(d3.plotable.LabelBox('label', histoLabel));

    if(histFail!=true) {
	if (opt.type == "H1D" || opt.type == "H1F") {		
	    var info = [
			['Entries', opt.numberEntries],
			['Mean', opt.mean],
			['RMS', opt.RMS],
			];
	    var ratio = myWidth/myHeight;
	    var statbox_size = [myWidth*0.35,myHeight*0.22];
	    var statbox_pos = [myWidth*0.62,myHeight*0.015];
	    if (ratio > 1.33) {
		statbox_size[1] = myHeight*0.35;
	    } //else {
	    //		statbox_size = [myWidth*0.3,myWidth*0.14];
	    //	    }
	    if (myWidth>600 && myHeight>400) {
		statbox_size[0] = myWidth*.3;
		statbox_size[1] = myHeight*.2;
	    } else if (myWidth<300 && myHeight<200) {
		statbox_size[0] = myWidth*.35;
		statbox_size[1] = myHeight*.5;
	    } else if (myWidth>550 && myHeight>550) {
		statbox_size[0] = myWidth*.35;
		statbox_size[1] = myHeight*.15;
	    }
	    chart.addOrnament(d3.plotable.TextBox('info', info, {x:statbox_pos[0], y:statbox_pos[1], width:statbox_size[0], height:statbox_size[1]}));
	    chart.addPlotable(d3.plotable.Histogram('histogram', data));

	
	} else if (opt.type == "H2D" || opt.type == "H2F"){

	    chart.addPlotable(d3.plotable.Histogram2D('histogram', data));

	    
	} else if (opt.type == "Profile"){

	    chart.addPlotable(d3.plotable.ProfileChart('histogram', data, {showPoints: true, showUncertainties: true}));

	}
    } else {
//	console.log("I'm here");
//	chart.addPlotable(d3.plotable.Histogram('histogram', empty_data));
//	chart.addOrnament(d3.plotable.LabelBox('sigFail', 'Data Failed', {x:0.7*myWidth, y:0.15*myHeight, color:"#ff0000", bkg:"#ffcabd"}));	    

    }

//    console.log("ref data = ", referenceData);
    var button = $("#changeReferenceMode");
    if(button.data("state") == "activated") {
	if(refFail!=true) {
	    console.log("I'm here in the reference");

	    if (opt.type == "H1D" || opt.type == "H1F") {		
		console.log("I'm here in h1d ref");
		chart.addPlotable(d3.plotable.Histogram('reference', referenceData, refopt));		    
	    } else if (opt.type == "Profile"){	    
		chart.addPlotable(d3.plotable.ProfileChart('reference', referenceData, $.extend(true, {}, refopt, {showPoints: true, showUncertainties: true}) ) );
	    }
	} else {


//	    chart.addPlotable(d3.plotable.Histogram('histogram', empty_data));
//	    chart.addOrnament(d3.plotable.LabelBox('refFail', 'Reference Failed', {x:0.7*myWidth, y:0.15*myHeight+22, color:"#ff0000",bkg:"#ffcabd"}));
	}
	    
    }



  };

  // Redraw histograms in the list
  var redrawHistograms = function()
  {
    for(var i = 0; i < localCache.listOfHistogramData.length; i++) {
      var histoContent = localCache.listOfHistogramData[i] ;
      
      // delete container cache
      histoContent.container.html('');;

      drawHistogram(histoContent.container,
        histoContent.formattedData,
        histoContent.formattedRefData,
	histoContent.options,
	histoContent.refoptions,
        histoContent.histFail,
        histoContent.refFail
      );		
    }
  };


  // Display a histogram, described by `data`, in `container`.
  // Accepts:
  //   data: An object describing the histogram
  //   container: A jQuery object in which to draw the histogram
  // Returns:
  //   undefined
  //  var displayHistogram = function(data, reference_data, refNormalisation, container, histFail, refFail) {
  var displayHistogram = function(result) {
 
      //    console.log("got data = ", result);

    var refNormalisation = result["refNormalisation"];
    var container = result["el"]
    
    var formattedData = [];
    var name, 
    type, 
    title, 
    values, 
    uncertainties, 
    axisTitles= [], 
    numberEntries, 
    integral, 
    mean, 
    RMS, 
    key_name;//, skewness;
    var histoDB_options = result["options"];
    console.log("options :: ", histoDB_options);

    //    if(histFail==false){

    //    title = result["showname"];
    var canvassize = [result["canvaswidth"],result["canvaswidth"]];
    if(result["data"]["success"]){
	var data = result["data"]["data"];
	var key_data = data['key_data'];

	name = key_data['name'];
	type = key_data['type'];
	//cannot load here the title// 
	//	title = data['key_title'];
	values = key_data['values'];
	uncertainties = key_data['uncertainties'];
	axisTitles = key_data['axis_titles'];      
	numberEntries = key_data['numberEntries'];
	integral = key_data['integral'];
	mean = key_data['mean'];
	RMS = key_data['RMS'];
	key_name = data['key_name'];
	//      skewness = key_data['skewness'];
	var xbinning, 
	    ybinning;

	if (type == "H1D" || type == "H1F" || type == "Profile" ){
	    xbinning = key_data['binning'];
	    
	}else if (type == "H2D" || type == "H2F"){
	    xbinning = key_data['xbinning'];
	    ybinning = key_data['ybinning'];
	}
	

	var v, binCenter, uLow, uHigh;
	console.log(">>>>>> TYPE ::",type);
	if (type == "H1D" || type == "H1F" || type == "Profile"){		    

	    for (var i = 0; i < values.length; i++) {
		if (type == "H1D" || type == "H1F" ){		    
		    var bins = xbinning[i];
		    
		    formattedData.push({
			    xlow: bins[0],
				xhigh: bins[1],
				y: key_data['values'][i],
				yerr: uncertainties[i]
				});
		}else if (type == "Profile"){
		    var bins = xbinning[i];
		    formattedData.push({
			    x: bins[0]+(bins[1]-bins[0])/2.,
				xerr: [(bins[1]-bins[0])/2.,(bins[1]-bins[0])/2.],
				y: values[i],
				yerr: uncertainties[i]
				});
		}

		
	    }
	} else if (type == "H2D" || type == "H2F") {

	    for (var i = 0; i < xbinning.length; i++) {
		var xbins = xbinning[i];

		for (var j = 0; j < ybinning.length; j++) {
	    
		    var ybins = ybinning[j];
		    formattedData.push({
			    xlow: xbins[0],
				xhigh: xbins[1],
				ylow: ybins[0],
				yhigh: ybins[1],				
				z: key_data['values'][i*ybinning.length + j],
				elow: uncertainties[i*ybinning.length + j],
				eup: uncertainties[i*ybinning.length + j]
				});		    
		}
	    }
	}
    } else { //no data in the container - problem in loading the histogram 
	//	title = result["showname"];
	axisTitles[0] = "";
	axisTitles[1] = ""; 
	numberEntries = 0;
	mean = 0;
	RMS = 0; 
	key_name = result["histogram"];  
	type = "H1D";
    }



    // Binning of the reference histogram (Only 1D histograms have references)  
    var key_ref = "";
    var refbinning, refvalues, refuncertainties, refnumberEntries, refintegral;
    //    if (refFail == false){
    if (result["refdata"]["success"]){
	var reference_data = result["refdata"]["data"];
	if (reference_data['key_data']) {
	    key_ref = reference_data['key_data'];
	    refbinning = key_ref['binning'];
	    refvalues = key_ref['values'];
	    refuncertainties = key_ref['uncertainties'];
	    refnumberEntries = key_ref['numberEntries'];
	    refintegral = key_ref['integral'];
	}
    }

    var formattedRefData = [];
    //check if data-reference != ""
    if (null != refvalues) {
      var factor = 1;
      //check normalisation mode, if not specified normalise anyway (to be corrected)
      if(constants.s_Entries == refNormalisation) {
        factor = numberEntries/refnumberEntries;
      } else if(constants.s_Area == refNormalisation) {
	factor = integral/refintegral;
      } else if(constants.s_NoNormalization != refNormalisation) {
	factor = integral/refintegral;
      }
      for (var i = 0; i < refvalues.length; i++) {
	  if (type == "H1D" || type == "H1F"){		    
	      var bins = refbinning[i];
	      formattedRefData.push({
	          xlow: bins[0],
		  xhigh: bins[1],
		  y: factor*key_ref['values'][i],
		  yerr: [factor*refuncertainties[i][0],factor*refuncertainties[i][1]]
	       });

	  }else if (type == "Profile"){
	      var bins = refbinning[i];
	      formattedRefData.push({
		      x: bins[0]+(bins[1]-bins[0])/2.,
			  xerr: [(bins[1]-bins[0])/2.,(bins[1]-bins[0])/2.],
			  y: key_ref['values'][i],
			  yerr: refuncertainties[i]
			  });
	  }

      }	
    }


    var local_options = {
//      run : key_ref['run_number'],
//      title: result["showname"];,
//      canvassize: canvassize,
//      xAxis : histoDB_options["label-x"],
//      yAxis : histoDB_options["label-y"],
//      top-label : histoDB_options["label-histo"],
//      cx : histoDB_options["center-x"],
//      cy : histoDB_options["center-y"],
//      sx : histoDB_options["center-x"],
//      sy : histoDB_options["center-x"],
//      xAxis: {
//	    title: axisTitles[0]
//      },
//      yAxis: {
//	    title: axisTitles[1]
//      },
      showUncertainties: true,
      color: "black",
      numberEntries: numberEntries,
      mean: mean,
      RMS: RMS,
      key_name: key_name,
      type: type
    };

    var options = $.extend(true, {}, result["options"],local_options);
    console.log("options :: ",options);

    var refoptions =  $.extend(true,{},options);		
    refoptions.color = "red"; // This will be dinamically set using the HistogramDB database

    // Remove the spinner
    container.find('.spinner').remove();

    // Save histogram content for redrawing!
    var histoContent =
    {
      container: container,
      formattedData: formattedData,
      formattedRefData: formattedRefData,
      options: options,
      refoptions: refoptions,
      histFail: !result["data"]["success"], 
      refFail: !result["refdata"]["success"]
    };

    localCache.listOfHistogramData[localCache.listOfHistogramData.length] = histoContent;

    // Draw the histogram in the container
    drawHistogram(container, formattedData, formattedRefData, options, refoptions, !result["data"]["success"], !result["refdata"]["success"]);
  };

  // Fetches and draws the named `histogram`, residing in `file`, in to the `container`.
  // Accepts:
  //   histogram: String of the histogram's full path key name with in the file
  //   file: String of the file name
  //   container: jQuery element the histogram should be drawn in to. Any existing content will be replaced.



  var loadHistograms = function(list) {
      //      console.log("length = " , list.elements.length)
      if (list.elements.length > 0) {
	  var url = '/tasks_bp/get_keys_from_list';
	  var histData = "";
	  var histFail = false;
	  var request = $.ajax(url, {
		  type: 'POST',
		  async : true,
		  timeout: 4000,
		  tryCount : 0,
		  retryLimit: 2,
		  contentType: 'application/json; charset=utf-8',
		  dataType: 'json',
		  data: JSON.stringify(list)
	      })
	  .done(function(job) {		      
		  // merge the list with data 
		  //		  var merge = list.elements.map(function(inlist){
		  list.elements.map(function(inlist){
			  var ret;
			  $.each( job['elements'], function(k, results) { 
				  
				  if(results.index === inlist.index) {
				      ret = $.extend({},results,inlist);
				      console.log("result = ", ret);
				      
				      return false;
				  }
			      });
			  displayHistogram(ret);
			  //			  return ret;
		      });
		  
		  

	      })
	  .fail(function(xhr, ajaxOptions, thrownError) {
		  var failMsg = '<p>There was a problem retrieving histograms for this pafe '
		  + '<code>' + 'PAGENAME' + '</code>'
		  + '. Please contact the administrator.</p>'
		  + thrownError;


		  if(ajaxOptions == 'timeout' || ajaxOptions == 'error') {
		      this.tryCount++;
		      if(this.tryCount <= this.retryLimit) {
			  $.ajax(this);
			  return;
		      }
		      var check = confirm('We have tried ' + this.retryLimit + ' times to do this and the server has not responded. Do you want to try again?');
		      if(check) {
			  this.timeout = 200000;
			  $.ajax(this);
			  return;
		      } else {
			  alert("JSON Error:" + thrownError + "; Page not reachable");
			  //			  displayFailure(container, failMsg);

			  return;
		      }
		  }   



		  //		  displayFailure(container, failMsg);
	      });     
	  

      }
  };

  // Page-specific modules
  var pages = {
    home: {
      init: function() {
        WebMonitor.log('home.init');
        // Or use pages.home.util
        this.util('Hello, World!');
      },
      // You don't have to put everything inside an `init`
      util: function(text) {
        WebMonitor.log('Utility function printing: ' + text);
      }
    }
  };

  // Initialise the monitoring app
  var init = function(pageModule) {
    WebMonitor.init(pageModule, pages);
    
    var $main = $('#main');
    
    var list = { elements : []};
    // Find any elements requiring histograms from files and load them
    var svgcanvas = $('#svg-canvas');
    svgcanvas.css('min-width','1200px');
    svgcanvas.css('display','inline-block');
//    svgcanvas.css('display','inline-block');
//    svgcanvas.css('position','relative');
    svgcanvas.css('width','100%');
//    svgcanvas.css('padding-bottom','100%');
//    svgcanvas.css('vertical-align','top');
    svgcanvas.css('overflow','hidden');

    //("display: inline-block; position: relative; width: 100%; padding-bottom: 100%; vertical-align: middle; overflow: hidden;" );
    var canvasheight = svgcanvas.height();
    var canvaswidth = svgcanvas.width();

    if (canvaswidth<1200) canvaswidth = 1200;
    
    $main.find('.histogram').each(function(index, el) {
	    
      var $el = $(el),
      file = $el.data('file'),
      histogram = $el.data('histogram'),      
      hid = $el.data('hid'),
      referenceFile = $el.data('reference-file'),//reference file
      reference = $el.data('reference'),//reference name in reference file
      refNormalisation = $el.data('refnormalisation'),
      showname = $el.data('showname');

      // Histogram information
      var labx = $el.data("lab-x"),
	  laby = $el.data("lab-y"),
	  labhisto = $el.data("lab-histo"),
	  labid = $el.data("label-id"),
	  centerx = $el.data("center-x"),
	  centery = $el.data("center-y"),
	  sizex = $el.data("size-x"),
	  sizey = $el.data("size-y");
      
      if (file && histogram) {
        WebMonitor.appendSpinner(el);

	var options = {
	    "xAxis" : labx,
	    "yAxis" : laby,
	    "label" : histogram,
	    "center-x" : centerx,
	    "center-y" : centery,
	    "size-x" : sizex,
	    "size-y" : sizey,
	    "canvassize" : [canvaswidth, canvaswidth*0.5],
	    "title" : showname
	};
	list.elements.push({
		"index" : index,
		"file" : file,
		"histogram" : histogram,
		"showname" : showname,
		"hid" : hid,
		"referenceFile" : referenceFile,
		"reference" : reference,
		"refNormalisation" : refNormalisation, 
		"el" : $el,
		"options" : options
//		"canvaswidth" : canvaswidth,
//		"canvasheight" : canvaswidth*0.5		    
		});
      }
  });
    
  loadHistograms(list);

    // Add datepicker to appropriate fields
    //    $main.find('.input-daterange').datepicker(WebMonitor.settings.datepickerDefaults);
  };

  return {
      init: init,
      redrawHistograms : redrawHistograms
      };
})(window);

$(function() {
  // Adjust some WebMonitor settings before initialisation
  WebMonitor.settings.debug = false;
  OfflineApp.init(activePage);
});
