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
      listOfHistogramData: []
  };

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
//    console.log("in drawHistogram", histFail, refFail);
//    console.log("data = ", data);
//    console.log("referenceData = ", referenceData);

    var opt = $.extend(true, {}, WebMonitor.settings.histogramDefaults, options);
    var refopt = $.extend(true, {}, WebMonitor.settings.histogramDefaults, refOptions);
    var xLabel ="", yLabel="", histoLabel ="Failed";

    if (histFail!=true) {
	//	console.log("in getopt parts", histFail, refFail);
	
	var optionsName = 'OPTIONS_FOR_'+opt.title;
	var histoOptions = document.getElementById(optionsName);
//	console.log("keyname = ",opt.key_name);
//	console.log("optionsName = ",optionsName);
//	console.log("histoOptions is null = ",histoOptions==null);
//	console.log("histoOptions",histoOptions);
	if (histoOptions!=null) {
	    xLabel = histoOptions.getAttribute('data-lab-x');
	    yLabel = histoOptions.getAttribute('data-lab-y');
	    histoLabel = histoOptions.getAttribute('data-lab-histo');
	}
    } else if (refFail!=true) {
	//	console.log("in ref getopt parts", histFail, refFail);
	
        var optionsName = 'OPTIONS_FOR_'+opt.key_name;
        var histoOptions = document.getElementById(optionsName);
        if (histoOptions!=null) {
	    xLabel = histoOptions.getAttribute('data-lab-x');
	    yLabel = histoOptions.getAttribute('data-lab-y');
	    histoLabel = histoOptions.getAttribute('data-lab-histo');
	}
    }

    if (opt.type == "H1D") {
	
	var chart = d3.select(container.get()[0]).append('svg')
	.attr('width', container.width())
	.attr('height', container.height())
	.chart('AxesChart')
	.xAxisLabel(xLabel)
	.yAxisLabel(yLabel);
	
	var myWidth = container.width();
	var myHeight = container.height();
	var info = [
		    ['Entries', opt.numberEntries],
		    ['Mean', opt.mean],
		    ['RMS', opt.RMS],
		    ];
	
	
	chart.addOrnament(d3.plotable.LabelBox('label', histoLabel));
	if(histFail!=true) {
	    chart.addOrnament(d3.plotable.TextBox('info', info, {x:0.62*myWidth, y:0.015*myWidth}));
	    chart.addPlotable(d3.plotable.Histogram('histogram', data));
	} else {
	    chart.addOrnament(d3.plotable.LabelBox('sigFail', 'Data Failed', {x:0.7*myWidth, y:0.15*myHeight, color:"#ff0000", bkg:"#ffcabd"}));
	    
	} 
	var button = $("#changeReferenceMode");
	if(button.data("state") == "activated") {
	    if(refFail!=true) {
		chart.addPlotable(d3.plotable.Histogram('reference', referenceData, refOptions));
	    } else {
		chart.addOrnament(d3.plotable.LabelBox('refFail', 'Reference Failed', {x:0.7*myWidth, y:0.15*myHeight+22, color:"#ff0000",bkg:"#ffcabd"}));
	    }
	    
	}
	
    } else if (opt.type == "H2D"){
        var histo2D = d3.select(container.get()[0]).append('svg')
          .attr('width', container.width())
          .attr('height', container.height())
          .chart('AxesChart')
          .xAxisLabel(xLabel)
          .yAxisLabel(yLabel)
          .animate(false);
        histo2D.addOrnament(d3.plotable.LabelBox('label', histoLabel));
        if(histFail!=true){	
	      histo2D.addPlotable(d3.plotable.Histogram2D('histogram', data));
        }else{
              histo2D.addOrnament(d3.plotable.LabelBox('sigFail', 'Run Failed', {x:0.7*myWidth, y:0.15*myHeight, color:"#ff0000", bkg:"#ffcabd"}));
        }

    } else if (opt.type == "Profile"){
        var profile = d3.select(container.get()[0]).append('svg')
          .attr('width', container.width())
          .attr('height', container.height())
          .chart('AxesChart')
          .xAxisLabel(xLabel)
          .yAxisLabel(yLabel)
          .animate(false);
        profile.addOrnament(d3.plotable.LabelBox('label', histoLabel));
        if(histFail!=true){      
	    profile.addPlotable(d3.plotable.ProfileChart('histogram', data, {showPoints: true, showUncertainties: true}));
        }else{
          profile.addOrnament(d3.plotable.LabelBox('sigFail', 'Data Failed', {x:0.7*myWidth, y:0.15*myHeight, color:"#ff0000", bkg:"#ffcabd"}));
        }
	var button = $("#changeReferenceMode");
	if(button.data("state") == "activated") {
	    if(refFail!=true) {
		profile.addPlotable(d3.plotable.ProfileChart('reference', referenceData, $.extend(true, {}, refopt, {showPoints: true, showUncertainties: true}) ) );
	    } else {
		profile.addOrnament(d3.plotable.LabelBox('refFail', 'Reference Failed', {x:0.7*myWidth, y:0.15*myHeight+22, color:"#ff0000",bkg:"#ffcabd"}));
	    }
	    
	}

    }

  };

  

  // Redraw histograms in the list
  var redrawHistograms = function(referenceState)
  {
    for(var i = 0; i < localCache.listOfHistogramData.length; i++) {
      var histoContent = localCache.listOfHistogramData[i] ;
      

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
    var name, type, title, values, uncertainties, axisTitles= [], numberEntries, integral, mean, RMS, key_name;//, skewness;
    
    //    if(histFail==false){
    if(result["data"]["success"]){
	var data = result["data"]["data"];
	var key_data = data['key_data'];

	name = key_data['name'];
	type = key_data['type'];
	title = data['key_title'];
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
	console.log("Type == " , type);
	if (type == "H1D" || type == "Profile" ){
	    xbinning = key_data['binning'];
	    
	}else if (type == "H2D"){
	    xbinning = key_data['xbinning'];
	    ybinning = key_data['ybinning'];
	}
	

	var v, binCenter, uLow, uHigh;
    
	if (type == "H1D" || type == "Profile"){		    

	    for (var i = 0; i < values.length; i++) {
		if (type == "H1D"){		    
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
	} else if (type == "H2D") {

	    for (var i = 0; i < xbinning.length; i++) {
		var xbins = xbinning[i];

		for (var j = 0; j < ybinning.length; j++) {
	    
		    var ybins = ybinning[j];
		    formattedData.push({
			    xlow: xbins[0],
				xhigh: xbins[1],
				ylow: ybins[0],
				yhigh: ybins[1],				
				z: key_data['values'][i],
				elow: uncertainties[i],
				eup: uncertainties[i]
				});		    
		}
	    }
	}
    } else { //no data in the container - problem in loading the histogram 
	title = "Data not loaded";
	axisTitles[0] = "";
	axisTitles[1] = ""; 
	numberEntries = 0;
	mean = 0;
	RMS = 0; 
	key_name = ""; 
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
	  if (type == "H1D"){		    
	      var bins = refbinning[i];
	      formattedRefData.push({
	          xlow: bins[0],
		  xhigh: bins[1],
		  y: factor*key_ref['values'][i],
		  yerr: [factor*refuncertainties[i][0],factor*refuncertainties[i][1]]
	       });

	  }else if (type == "Profile"){
	      var bins = xbinning[i];
	      formattedRefData.push({
		      x: bins[0]+(bins[1]-bins[0])/2.,
			  xerr: [(bins[1]-bins[0])/2.,(bins[1]-bins[0])/2.],
			  y: values[i],
			  yerr: uncertainties[i]
			  });
	  }

      }	
    }


    var options = {
	//      run : key_ref['run_number'],
      title: title,
      xAxis: {
	    title: axisTitles[0]
      },
      yAxis: {
	    title: axisTitles[1]
      },
      showUncertainties: true,
      color: "black",
      numberEntries: numberEntries,
      mean: mean,
      RMS: RMS,
      key_name: key_name,
      type: type
    };


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
  var loadHistogramFromFileIntoContainer = function(histogram, file, hid, reference, referenceFile, refNormalisation, container) {


    // Load reference data if reference data is defined
    var referenceData = "";
    var refFail = false; 
    if (reference != "") {
	var referenceUrl = '/tasks_bp/get_key_from_file';
	var referenceRequest = $.ajax(referenceUrl, {
		type: 'POST',
		contentType: 'application/json; charset=utf-8',
		dataType: 'json',
		data: JSON.stringify({
			filename: referenceFile, 
			key_name: reference, 
			is_reference: true})
	    })
	    .done(function(job) {
		    if (job['success']) {
			referenceData = job['data'];	
		    } else {
			refFail = true;
			referenceData = "";
		    }
		})
	    .fail(function(message) {
		    var failMsg = '<p>There was a problem retrieving the REFERENCE histogram '
		    + '<code>' + reference + '</code>'
		    + ' from file '
		    + '<code>' + file + '</code>'
		    + '. Please contact the administrator.</p>'
		    + message;
		    displayFailure(container, failMsg);
		    refFail = true;
		});

//      var referenceTask = WebMonitor.createTask('get_key_from_file', {filename: referenceFile, key_name: reference});
//      referenceTask.done(function(job) {
//        referenceData = job['result']['data'];	
//      });
//      referenceTask.fail(function(message) {
//        var failMsg = '<p>There was a problem retrieving the REFERENCE histogram '
//          + '<code>' + reference + '</code>'
//          + ' from file '
//          + '<code>' + file + '</code>'
//          + '. Please contact the administrator.</p>'
//          + message;
//        displayFailure(container, failMsg);
//          refFail = true;
//      });
    }


    // Request histogram from server

    var url = '/tasks_bp/get_key_from_file';
    var histData = "";
    var histFail = false;
    var request = $.ajax(url, {
	    type: 'POST',
	    contentType: 'application/json; charset=utf-8',
	    dataType: 'json',
	    data: JSON.stringify({
		    filename: file, 
		    key_name: histogram, 
		    is_reference: false})
	})
    .done(function(job) {
//	    console.log("getting ",histogram);
//	    console.log("job status ",job['success']);
	    if (job['success']) {
		histData = job['data'];	
	    } else {
		histFail = true;
		histData = "";
	    }

	    displayHistogram(histData, referenceData, refNormalisation, container, histFail, refFail);

	})
    .fail(function(message) {
	    var failMsg = '<p>There was a problem retrieving histogram '
	    + '<code>' + histogram + '</code>'
	    + ' from file '
	    + '<code>' + file + '</code>'
	    + '. Please contact the administrator.</p>'
	    + message;
	    displayFailure(container, failMsg);
	    histFail = true;
	    displayHistogram("", referenceData, refNormalisation, container, histFail, refFail);
	});     

  };

//    var task = WebMonitor.createTask('get_key_from_file', {filename: file, key_name: histogram});
//    var histFail = false;
//    task.done(function(job) {
//        console.log("getting ",histogram);
//        displayHistogram(job['result']['data'], referenceData, refNormalisation, container, histFail, refFail);
//    });
//    task.fail(function(message, job) {
//      var failMsg = '<p>There was a problem retrieving histogram '
//      + '<code>' + histogram + '</code>'
//      + ' from file '
//      + '<code>' + file + '</code>'
//      + '. Please contact the administrator.</p>'
//      + message;
//      displayFailure(container, failMsg);
//       histFail = true;
//       displayHistogram("", referenceData, refNormalisation, container, histFail, refFail);
//    });     
//  };



  var loadHistograms = function(list) {
      //      console.log("length = " , list.elements.length)
      if (list.elements.length > 0) {
	  var url = '/tasks_bp/get_keys_from_list';
	  var histData = "";
	  var histFail = false;
	  var request = $.ajax(url, {
		  type: 'POST',
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
				      
				      return false;
				  }
			      });
			  displayHistogram(ret);
			  //			  return ret;
		      });
		  
		  

	      })
	  .fail(function(message) {
		  var failMsg = '<p>There was a problem retrieving histograms for this pafe '
		  + '<code>' + 'PAGENAME' + '</code>'
		  + '. Please contact the administrator.</p>'
		  + message;
		  displayFailure(container, failMsg);
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
    $main.find('.histogram').each(function(index, el) {
	    
      var $el = $(el),
      file = $el.data('file'),
      histogram = $el.data('histogram'),
      hid = $el.data('hid'),
      referenceFile = $el.data('reference-file'),//reference file
      reference = $el.data('reference'),//reference name in reference file
      refNormalisation = $el.data('refnormalisation');
      if (file && histogram) {
        WebMonitor.appendSpinner(el);
	 //        loadHistogramFromFileIntoContainer(histogram, file, hid, reference, referenceFile, refNormalisation, $el);
	list.elements.push({
		"index" : index,
		"file" : file,
		"histogram" : histogram,
		"hid" : hid,
		"referenceFile" : referenceFile,
		"reference" : reference,
		"refNormalisation" : refNormalisation, 
		"el" : $el			
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
