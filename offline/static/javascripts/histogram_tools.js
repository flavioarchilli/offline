
// Histogram tools

// Save recursively all the histograms
function saveAllHistograms() {
  var elm = $('#histoContainer').find("svg").each( 
    function() {
      var name = $(this).parent().parent().find(".histoTitle").text() + ".png";
      saveSvgAsPng($(this)[0], name);
    });
}

