// This structure is similar to that used by WebMonitor.js.
// You have access to both the WebMonitor object and activePage (if the page
// is being served by the catchall.serve_page route), which you can use to
// determine what page you're own, and hence what things need doing.
var ExampleApp = (function(window, undefined) {
  'use strict';

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
    },
    examples: {
      init: function() {
        WebMonitor.log('examples.init');
      },
      table: {
        init: function() {
          WebMonitor.log('examples.table.init');
        }
      },
      singleLayout: {
        init: function() {
          WebMonitor.log('examples.singleLayout.init');
        }
      }
    }
  };

  // Initialise the monitoring app
  var init = function(pageModule) {
    WebMonitor.init(pageModule, pages);
  };

  return {
    init: init
  };
})(window);

$(function() {
  // Adjust some WebMonitor settings before initialisation
  WebMonitor.settings.debug = true;
  ExampleApp.init(activePage);
});
