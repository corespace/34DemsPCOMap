var globals;

var Globals = class {
  constructor(map, geocoder) {
    this.map = map;
    this.geocoder = geocoder;
  }

  GetMap() {
    return this.map;
  }

  GetGeocoder() {
    return this.geocoder;
  }
}


var InitMap = function() {
  var map;
  var initPoint = {lat: 47.47, lng: -122.41}
  geocoder = new google.maps.Geocoder();
  map = new google.maps.Map(document.getElementById('map'), {
    center: initPoint,
    zoom: 11
  });
  globals = new Globals(map, geocoder);
  DrawAllPrecincts();
}

var GeoCodeAddress = function() {
  var address = document.getElementById('address').value;
  globals.GetGeocoder().geocode( { 'address': address}, function(results, status) {
    if (status == 'OK') {
      globals.GetMap().setCenter(results[0].geometry.location);
      var marker = new google.maps.Marker({
          map: globals.GetMap(),
          position: results[0].geometry.location
      });
    } else {
      alert('Geocode was not successful for the following reason: ' + status);
    }
  });
}

var DrawAllPrecincts = function() {
  var url = "https://xv1zwa82p7.execute-api.us-east-1.amazonaws.com/dev/precincts";

  globals.GetMap().data.loadGeoJson(url);
  //Set any precinct that has no PCO to red
  globals.GetMap().data.setStyle(function(feature) {
    var pco = feature.getProperty('pco');
    var color = pco ? 'white' : 'red';
    return {
      fillColor: color,
    };
  });
}