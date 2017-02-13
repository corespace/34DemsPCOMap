var globals;

var Globals = class {
  constructor(map, geocoder, infoWindow) {
    this.map = map;
    this.geocoder = geocoder;
    this.infoWindow = infoWindow;
  }

  GetMap() {
    return this.map;
  }

  GetGeocoder() {
    return this.geocoder;
  }

  GetInfoWindow() {
    return this.infoWindow;
  }
}


var InitMap = function() {
  var initPoint = {lat: 47.47, lng: -122.41}

  var geocoder = new google.maps.Geocoder();
  var infoWindow = new google.maps.InfoWindow()
  var map = new google.maps.Map(document.getElementById('map'), {
    center: initPoint,
    zoom: 11
  });
  google.maps.event.addListener(map,'click',function() {
        globals.GetInfoWindow().close();
  });

  globals = new Globals(map, geocoder, infoWindow);
  DrawAllPrecincts();
}

var GeoCodeAddress = function() {
  var address = document.getElementById('address-box').value;
  globals.GetGeocoder().geocode( { 'address': address}, function(results, status) {
    if (status == 'OK') {
      globals.GetMap().setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: globals.GetMap(),
          position: results[0].geometry.location
      });
      globals.GetInfoWindow().close();
      //CreateInfoWindow();
      //globals.GetInfoWindow().open(globals.GetMap(), marker);
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

var DrawAllPrecincts = function() {
  var url = "https://api.34dems.net/precincts";

  globals.GetMap().data.loadGeoJson(url);
  //Set any precinct that has no PCO to red
  globals.GetMap().data.setStyle(function(feature) {
    var pco = feature.getProperty('pco');
    var color = pco ? 'white' : '#dd9933';
    return {
      fillColor: color,
    };
  });

  //if user clicks, show PCO info
  globals.GetMap().data.addListener('click', function(event){
    CreateInfoWindow(event.feature);
    var anchor = new google.maps.MVCObject();
    anchor.set("position", event.latLng)
    globals.GetInfoWindow().open(globals.GetMap(), anchor);
  });
}


var CreateInfoWindow = function(feature) {
    var pcoContent = '<div id="content">'
      + '<h3>Precinct: ' + feature.getProperty('name') + '</h3>';
    var pcoInfo = feature.getProperty('pco');

    if(pcoInfo) {
      pcoContent = pcoContent  +  
      '<h5>' + pcoInfo['first'] + ' ' + pcoInfo['last'] + '</h5>';
    } else {
      pcoContent = pcoContent + '<p> No PCO currently.</p>' + 
        '<a href="http://www.34dems.org/get-active/pco/"> Click here to be appointed!</a>';
    }

    pcoContent = pcoContent + '</div>';

    //Set Info Window
    globals.GetInfoWindow().setContent(pcoContent);
}


