
var options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
  };

  function success(pos) {
    var crd = pos.coords;
    var latnfield = document.getElementById("latn");
    var lonnfield = document.getElementById("lonn");
    latnfield.value = crd.latitude;
    lonnfield.value = crd.longitude;
  };

  function error(err) {
    console.warn('ERROR(' + err.code + '): ' + err.message);
  };

  navigator.geolocation.getCurrentPosition(success, error, options);
