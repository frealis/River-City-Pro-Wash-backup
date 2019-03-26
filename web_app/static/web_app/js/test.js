
// Restrict phone number field to numbers 0 through 9
function keypress(event) {
  var keycode = event.which;
  console.log(event.which);
  if (keycode < 48 || keycode > 57) {
    return false;
  };
};