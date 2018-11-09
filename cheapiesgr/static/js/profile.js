var strength = {
  0: "Απαίσια",
  1: "Κακή",
  2: "Αδύναμη",
  3: "Καλή",
  4: "Πολύ δυνατή"
}

var password = document.getElementById('new-pwd');
var text = document.getElementById('password-strength-text');

password.addEventListener('input', function()
{
  var val = password.value;
  var result = zxcvbn(val);

  if(val !== "") {
    text.innerHTML = "Δύναμη Κωδικού: " + strength[result.score];
  }
  else {
    text.innerHTML = "Δεν έχετε εισάγει κωδικό";
  }
});
