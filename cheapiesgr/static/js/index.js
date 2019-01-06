// Geolocation
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

// Speech Recognition with webkitSpeechRecognition API
$('button[type!=submit]').click(function(event) { event.stopPropagation(); });

window.SpeechRecognition = window.webkitSpeechRecognition || window.SpeechRecognition;
let finalTranscript = '';
let recognition = new window.SpeechRecognition();

recognition.interimResults = true;
recognition.maxAlternatives = 10;
recognition.continuous = true;
recognition.lang = "el-GR";


recognition.onresult = (event) => {
  let interimTranscript = '';
  for (let i = event.resultIndex, len = event.results.length; i < len; i++) {
    let transcript = event.results[i][0].transcript;
    if (event.results[i].isFinal) {
      finalTranscript += transcript;
    } else {
      interimTranscript += transcript;
    }
  }

  document.getElementById('search').value = finalTranscript + interimTranscript;
}

recognition.onspeechend = (event) => {
  $("#search-form").submit();
}

function recognizeSpeech() {
  recognition.start();
}
