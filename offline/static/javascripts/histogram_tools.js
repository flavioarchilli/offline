
// Histogram tools

// Save recursively all the histograms
function saveAllHistograms() {
  console.log('inside saveAll');

  var elm = $('#svg-canvas').find("svg").each( 

    function() {
//      console.log("this = " + $(this).parent().parent().parent().text());
      var name = $(this).find(".histoTitle").text() + ".png";
      saveSvgAsPng($(this)[0], name);
    });
}

