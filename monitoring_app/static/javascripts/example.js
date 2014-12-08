// This structure is similar to that used by JobMonitor.js.
// You have access to both the JobMonitor object and activePage (if the page
// is being served by the catchall.serve_page route), which you can use to
// determine what page you're own, and hence what things need doing.
var ExampleApp = (function(window, undefined) {
  'use strict';

  // Display msg inside container, styled as a red error box
  // Accepts:
  //   container: jQuery element to insert msg into
  //   msg: HTML message to display inside container
  var displayFailure = function(container, msg) {
    container.html('<div class="alert alert-danger">' + msg + '</div>');
  };

  // Draw a histogram in the `container` using `options`.
  // Accepts:
  //   container: A jQuery object in which to draw the histogram
  //     If the jQuery object references multiple DOM nodes, the first is used
  //   data: An array of data points formatted for d3.chart.histogram
  //   options: Object of options passed to the plotting library
  //     Any present options override those in JobMonitor.settings.histogramDefaults
  // Returns:
  //   undefined
  var drawHistogram = function(container, data, options) {
    var opt = $.extend(true, {}, JobMonitor.settings.histogramDefaults, options);
    var chart = d3.select(container.get()[0]).append('svg')
      .attr('width', container.width())
      .attr('height', container.height())
      .chart('AxesChart')
      .xAxisLabel(opt.xAxis.title.text)
      .yAxisLabel(opt.yAxis.title.text);
    chart.addPlotable(d3.plotable.Histogram('histogram', data));
  };

  // Display a histogram, described by `data`, in `container`.
  // Accepts:
  //   data: An object describing the histogram
  //   container: A jQuery object in which to draw the histogram
  // Returns:
  //   undefined
  var displayHistogram = function(data, container) {
    var name = data['name'],
        title = data['title'],
        binning = data['binning'],
        values = data['values'],
        uncertainties = data['uncertainties'],
        axisTitles = data['axis_titles'];
    var v, binCenter, uLow, uHigh;
    // We need to manipulate the values slightly for d3.chart.histogram
    // See the d3.chart.histogram documentation for the specifics
    var formattedData = [];
    for (var i = 0; i < values.length; i++) {
      var bins = binning[i];
      formattedData.push({
        xlow: bins[0],
        xhigh: bins[1],
        y: data['values'][i],
        yerr: uncertainties[i]
      });
    }
    var options = {
      title: title,
      xAxis: {
        title: axisTitles[0]
      },
      yAxis: {
        title: axisTitles[1]
      }
    };
    // Remove the spinner
    container.find('.spinner').remove();
    // Draw the histogram in the container
    drawHistogram(container, formattedData, options);
  };

  // Fetches and draws the named `histogram`, residing in `file`, in to the `container`.
  // Accepts:
  //   histogram: String of the histogram's full path key name with in the file
  //   file: String of the file name
  //   container: jQuery element the histogram should be drawn in to. Any existing content will be replaced.
  var loadHistogramFromFileIntoContainer = function(histogram, file, container) {
      var task = JobMonitor.createTask('get_key_from_file', {filename: file, key_name: histogram});
      task.done(function(job) {
          displayHistogram(job['result']['data']['key_data'], container);
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
        JobMonitor.log('home.init');
        // Or use pages.home.util
        this.util('Hello, World!');
      },
      // You don't have to put everything inside an `init`
      util: function(text) {
        JobMonitor.log('Utility function printing: ' + text);
      }
    },
    examples: {
      init: function() {
        JobMonitor.log('examples.init');
      },
      table: {
        init: function() {
          JobMonitor.log('examples.table.init');
        }
      },
      singleLayout: {
        init: function() {
          JobMonitor.log('examples.singleLayout.init');
        }
      }
    }
  };

  // Initialise the monitoring app
  var init = function(pageModule) {
    JobMonitor.init(pageModule, pages);

    var $main = $('#main');

    // Find any elements requiring histograms from files and load them
    $main.find('.histogram').each(function(index, el) {
      var $el = $(el),
          file = $el.data('file'),
          histogram = $el.data('histogram');
      if (file && histogram) {
        JobMonitor.appendSpinner(el);
        loadHistogramFromFileIntoContainer(histogram, file, $el);
      }
    });

    // Add datepicker to appropriate fields
    $main.find('.input-daterange').datepicker(JobMonitor.settings.datepickerDefaults);
  };

  return {
    init: init
  };
})(window);

$(function() {
  // Adjust some JobMonitor settings before initialisation
  JobMonitor.settings.debug = true;
  ExampleApp.init(activePage);
});
