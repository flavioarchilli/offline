(function() {
  var out$ = typeof exports != 'undefined' && exports || this;

  var doctype = '<?xml version="1.0" standalone="no"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">';

  function inlineImages(callback) {
    var images = document.querySelectorAll('svg image');
    var left = images.length;
    if (left == 0) {
      callback();
    }
    for (var i = 0; i < images.length; i++) {
      (function(image) {
        if (image.getAttribute('xlink:href')) {
          var href = image.getAttribute('xlink:href').value;
          if (/^http/.test(href) && !(new RegExp('^' + window.location.host).test(href))) {
            throw new Error("Cannot render embedded images linking to external hosts.");
          }
        }
        var canvas = document.createElement('canvas');
        var ctx = canvas.getContext('2d');
        var img = new Image();
        img.src = image.getAttribute('xlink:href');
        img.onload = function() {
          canvas.width = img.width;
          canvas.height = img.height;
          ctx.drawImage(img, 0, 0);
          image.setAttribute('xlink:href', canvas.toDataURL('image/png'));
          left--;
          if (left == 0) {
            callback();
          }
        }
      })(images[i]);
    }
  }


  function styles(dom) {
    var used = "";
    var sheets = document.styleSheets;
    console.log(sheets);
    var defs = document.createElement('defs');

    for (var i = 0; i < sheets.length; i++) {

      try {	  
        if (!sheets[i].cssRules)
	    return defs;
      } catch(e) {
        if (e.name !== 'SecurityError')
	  throw e;
	return defs;
      }

//      var rules = sheets[i].cssRules;
//      console.log(rules);
//      if (rules == null) continue;
      for (var j = 0; j < sheets[i].cssRules.length; j++) {
        var rule = sheets[i].cssRules[j];
        if (typeof(rule.style) != "undefined") {
	    //          var elems = dom.querySelectorAll(rule.selectorText);
          var elems = dom.querySelectorAll(rule.selectorText);
          if (elems.length > 0) {
            used += rule.selectorText + " { " + rule.style.cssText + " }\n";
          }
        }
      }
    }

    var s = document.createElement('style');
    s.setAttribute('type', 'text/css');
    s.innerHTML = "<![CDATA[\n" + used + "\n]]>";


    defs.appendChild(s);
    return defs;
  }

  out$.svgAsDataUri = function(el, scaleFactor, cb) {
    scaleFactor = scaleFactor || 1;

    inlineImages(function() {
      var outer = document.createElement("div");
      var clone = el.cloneNode(true);
      var width = parseInt(clone.getAttribute("width"));
      var height = parseInt(clone.getAttribute("height"));
      console.log("clone width = ", width);
      var xmlns = "http://www.w3.org/2000/xmlns/";

      clone.setAttribute("version", "1.1");
      clone.setAttributeNS(xmlns, "xmlns", "http://www.w3.org/2000/svg");
      clone.setAttributeNS(xmlns, "xmlns:xlink", "http://www.w3.org/1999/xlink");
      clone.setAttribute("width", width * scaleFactor);
      clone.setAttribute("height", height * scaleFactor);
      clone.setAttribute("viewBox", "0 0 " + width + " " + height);
      outer.appendChild(clone);
      console.log("outer = ", outer);
      clone.insertBefore(styles(clone), clone.firstChild);

      var svg = doctype + outer.innerHTML;
      var uri = 'data:image/svg+xml;base64,' + window.btoa(unescape(encodeURIComponent(svg)));
      console.log("uri = ", uri);
      if (cb) {
        cb(uri);
      }
    });
  }

  out$.saveSvgAsPng = function(el, name, scaleFactor) {
    console.log("here, el = "+ el  +" name = " + name + " scale = ", scaleFactor);
    out$.svgAsDataUri(el, scaleFactor, function(uri) {
      var image = new Image();
      image.src = uri;
      image.onload = function() {
        var canvas = document.createElement('canvas');
        canvas.width = image.width;
        canvas.height = image.height;
        var context = canvas.getContext('2d');
        context.drawImage(image, 0, 0);

        var a = document.createElement('a');
        a.download = name;
        a.href = canvas.toDataURL('image/png');
        document.body.appendChild(a);
        a.click();
      }
    });
  }
})();
