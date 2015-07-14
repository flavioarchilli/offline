
// This structure is similar to that used by WebMonitor.js.
// You have access to both the WebMonitor object and activePage (if the page
// is being served by the catchall.serve_page route), which you can use to
// determine what page you're own, and hence what things need doing.
var OfflineApp = (function(window, undefined) {
  'use strict';

  // Display msg inside container, styled as a red error box
  // Accepts:
  //   container: jQuery element to insert msg into
  //   msg: HTML message to display inside container
  var displayFailure = function(container, msg) {
    container.html('<div class="alert alert-danger">' + msg + '</div>');
  };

  var constants = {
    s_Area: "AREA",
    s_Entries: "ENTR",
    s_NoReference: "NOREF",
    s_NoNormalization: "NONE"
  };


  var localChache = {
      listOfHistogram: []
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
  var drawHistogram = function(container, data, referenceData, options, refOptions) {
    var opt = $.extend(true, {}, WebMonitor.settings.histogramDefaults, options);

    var histoOptions = $(document.getElementById("OPTIONS_FOR_"+opt.key_name));

    var xLabel = histoOptions.data("label-x")
    var yLabel = histoOptions.data("label-y")
	
    var histoTitle = document.getElementById("LABEL_FOR_"+opt.key_name);
    $(histoTitle).text(opt.title.text);

    var chart = d3.select(container.get()[0]).append('svg')
      .attr('width', container.width())
      .attr('height', container.height())
      .chart('AxesChart')
      .xAxisLabel(opt.xAxis.title.text)
      .yAxisLabel(opt.yAxis.title.text);
    
    var info = [
      ['Entries', opt.numberEntries],
      ['Mean', opt.mean],
      ['RMS', opt.RMS],
    ];
	

    chart.addOrnament(d3.plotable.TextBox('info', info));
    chart.addPlotable(d3.plotable.Histogram('histogram', data));
	
    var button = $("#changeReferenceMode");
    if(button.data("state") == "activated")
      {
        chart.addPlotable(d3.plotable.Histogram('reference', referenceData, refOptions));
      }
  };



  // Redraw histograms in the list
  var redrawHistograms = function(referenceState)
  {
    for(var i = 0; i < OfflineApp.localChache.listOfHistogramData.length; i++) {
      var histoContent = OfflineApp.localChache.listOfHistogramData[i] ;
  		
      histoContent.container.empty();
  		
      drawHistogram(histoContent.container,
        histoContent.formattedData,
        histoContent.formattedRefData,
	histoContent.options,
	histoContent.refoptions
      );		
    }
  };


  // Display a histogram, described by `data`, in `container`.
  // Accepts:
  //   data: An object describing the histogram
  //   container: A jQuery object in which to draw the histogram
  // Returns:
  //   undefined
  var displayHistogram = function(data, referenceData, refNormalisation, container) {

    var name = data['name'],
      type = data['type'],
      title = data['title'],
      binning = data['binning'],
      values = data['values'],
      uncertainties = data['uncertainties'],
      axisTitles = data['axis_titles'],      
      numberEntries = data['numberEntries'],
      integral = data['integral'],
      mean = data['mean'],
      RMS = data['RMS'],
      key_name = data['key_name'],
      skewness = data['skewness'];
      
    var xbinning, 
      ybinning;

    if (type == "1D"){
      xbinning = data['binning'];
	    
    }else if (type == "2D"){
      xbinning = data['xbinning'];
      ybinning = data['ybinning'];
    }
	
    // Binning of the reference histogram (Only 1D histograms have references)	
    var refbinning = referenceData['binning'],
      refvalues = referenceData['values'],
      refuncertainties = referenceData['uncertainties'],
      refnumberEntries = referenceData['numberEntries'],
      refintegral = referenceData['integral'];
		  	  

    var v, binCenter, uLow, uHigh;
    // We need to manipulate the values slightly for d3.chart.histogram
    // See the d3.chart.histogram documentation for the specifics
    var formattedData = [];


    for (var i = 0; i < values.length; i++) {
      if (type == "1D"){		    
        var bins = xbinning[i];
	formattedData.push({
	  xlow: bins[0],
	  xhigh: bins[1],
	  y: data['values'][i],
	  yerr: uncertainties[i],
	});
      }
      else if (type == "2D"){
        var xbins = xbinning[i];
          ybins = ybinning[i];
	  
	formattedData.push({
	  xlow: xbins[0],
	  xhigh: xbins[1],
	  ylow: ybins[0],
	  yhigh: ybins[1],				
	  z: data['values'][i],
	  elow: uncertainties[i],
	  eup: uncertainties[i],
        });		    
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
	var bins = refbinning[i];
	  
	formattedRefData.push({
	  xlow: bins[0],
	  xhigh: bins[1],
	  y: factor*refvalues[i],
	  yerr: [factor*refuncertainties[i][0], factor*refuncertainties[i][1]],
	});
      }	
    }


    var options = {
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
      key_name: key_name
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
      refoptions: refoptions
    };    		
    OfflineApp.localChache.listOfHistogramData[OfflineApp.localChache.listOfHistogramData.length] = histoContent;

    // Draw the histogram in the container
    drawHistogram(container, formattedData, options);
  };

  // Fetches and draws the named `histogram`, residing in `file`, in to the `container`.
  // Accepts:
  //   histogram: String of the histogram's full path key name with in the file
  //   file: String of the file name
  //   container: jQuery element the histogram should be drawn in to. Any existing content will be replaced.
  var loadHistogramFromFileIntoContainer = function(histogram, file, hid, reference, referenceFile, refNormalisation, container) {


    // Load reference data if reference data is defined
    var referenceData = "";

    if (reference != "") {
      var referenceTask = WebMonitor.createTask('get_key_from_file', {filename: referenceFile, key_name: reference});
      referenceTask.done(function(job) {
        referenceData = job['result']['data']['key_data'];
      });
      referenceTask.fail(function(message) {
        var failMsg = '<p>There was a problem retrieving the REFERENCE histogram '
          + '<code>' + reference + '</code>'
          + ' from file '
          + '<code>' + file + '</code>'
          + '. Please contact the administrator.</p>'
          + message;
        displayFailure(container, failMsg);
      });
    }


    // Request histogram from server
    var task = WebMonitor.createTask('get_key_from_file', {filename: file, key_name: histogram});
    task.done(function(job) {
      displayHistogram(job['result']['data']['key_data'], referenceData, refNormalisation, container);
    });
    task.fail(function(message) {
      var failMsg = '<p>There was a problem retrieving histogram '
      + '<code>' + histogram + '</code>'
      + ' from file '
      + '<code>' + file + '</code>'
      + '. Please contact the administrator.</p>'
      + message;
      displayFailure(container, failMsg);
    });
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
        loadHistogramFromFileIntoContainer(histogram, file, hid, reference, referenceFile, refNormalisation, $el);
      }
    });

    // Add datepicker to appropriate fields
    //    $main.find('.input-daterange').datepicker(WebMonitor.settings.datepickerDefaults);
  };

  return {
    init: init
  };
})(window);

$(function() {
  // Adjust some WebMonitor settings before initialisation
  WebMonitor.settings.debug = true;
  OfflineApp.init(activePage);
});
