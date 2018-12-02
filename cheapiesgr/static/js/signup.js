var strength = {
  0: "Απαίσια",
  1: "Κακή",
  2: "Αδύναμη",
  3: "Καλή",
  4: "Πολύ δυνατή"
}

var password = document.getElementById('pwd');
var text = document.getElementById('password-strength-text');

password.addEventListener('input', function()
{
  var val = password.value;
  var result = zxcvbn(val);

  if(val !== "") {
    text.innerHTML = "Δύναμη Κωδικού: " + strength[result.score];
    if (result.score==0) {
      text.style.color = "crimson";
    }
    else if (result.score==1) {
      text.style.color = "darkorange";
    }
    else if (result.score==2) {
      text.style.color = "gold";
    }
    else if (result.score==3) {
      text.style.color = "lime";
    }
    else if (result.score==4) {
      text.style.color = "green";
    }
  }
  else {
    text.innerHTML = "";
  }
});
