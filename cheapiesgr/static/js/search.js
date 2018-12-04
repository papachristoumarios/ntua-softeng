
var options = {
    enableHighAccuracy: true,
    timeout: 5000,
    maximumAge: 0
  };

  function success(pos) {
    var crd = pos.coords;
    var latfield = document.getElementById("lat");
    var lonfield = document.getElementById("lon");
    latfield.value = crd.latitude;
    lonfield.value = crd.longitude;
  };

  function error(err) {
    console.warn('ERROR(' + err.code + '): ' + err.message);
  };

  navigator.geolocation.getCurrentPosition(success, error, options);
