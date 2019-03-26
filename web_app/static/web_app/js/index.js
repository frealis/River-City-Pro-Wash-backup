function keypress(event) {
  var keycode = event.which;
  console.log(event.which);
  if (keycode < 48 || keycode > 57) {
    return false;
  };
};

// document.addEventListener('DOMContentLoaded', () => {

//   var phone = document.querySelectorAll('.phone');

//   for (var i = 0; i < phone.length; i++) {
//     phone[i].addEventListener('keypress', function(event) {
//       return keypress(event);
//     });
//   };
// });