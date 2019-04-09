// Restrict phone number field to numbers 0 through 9
function noLetters(event) {
  var keycode = event.which;
  if (keycode < 48 || keycode > 57) {
    return false;
  };
};

// Restrict phone number extention field to exclude spaces
function noSpaces(event) {
  var keycode = event.which;
  if (keycode === 32) {
    return false;
  };
};

// Toggle navbar fixed-top class (mostly taken from CS50 class example on front 
// ends)
window.onscroll = () => {
  console.log('----');
  console.log('window.innerHeight: ', window.innerHeight);
  console.log('window.scrollY: ', window.scrollY);
  console.log('document.body.offsetHeight: ', document.body.offsetHeight);

  // 260 is the distance in pixels from the top of the screen to the top of the
  // navbar. Add 56 pixels worth of margin on top of the carosel section to 
  // account for the height of the navbar. The '.show' class is only added to 
  // the navbar when it is toggled on from collapsed/small screen mode.
  if (window.scrollY < 260) {
    document.querySelector('#nav_bar').classList.remove('fixed-top')
    document.querySelector('#nav_bar').classList.add('prevent_pushdown')
    // document.querySelector('#myCarousel').classList.remove('margin-top56')

    // if (document.querySelector('.show')) {
    //   anchor_points = document.querySelectorAll('.anchor-point')
    //   for (let i = 0; i < anchor_points.length; i++) {
    //     anchor_points[i].classList.add('anchor-336');
    //     if (anchor_points[i].classList.contains('anchor-56')) {
    //       anchor_points[i].classList.remove('anchor-56');
    //     };
    //   };
    // };

  } else if (window.scrollY >= 260) {
    document.querySelector('#nav_bar').classList.remove('prevent_pushdown')
    document.querySelector('#nav_bar').classList.add('fixed-top')
    // document.querySelector('#myCarousel').classList.add('margin-top56')

    // if (document.querySelector('.show')){
    //   anchor_points = document.querySelectorAll('.anchor-point')
    //   for (let i = 0; i < anchor_points.length; i++) {
    //     anchor_points[i].classList.add('anchor-56');
    //     if (anchor_points[i].classList.contains('anchor-336')) {
    //       anchor_points[i].classList.remove('anchor-336');
    //     };
    //   };
    // };
    
  };
};

document.addEventListener('DOMContentLoaded', function() {

  // Retrieve message from "Contact Us" form and submit
  document.querySelector('#send_message').onclick = () => {

    console.log('click');

    recaptcha = grecaptcha.getResponse();
    console.log(recaptcha);

    if (grecaptcha.getResponse() !== '') {

      // Initialize POST request, extract the CSRF value from the index.html DOM,
      // and put that into the header of the POST request
      const request = new XMLHttpRequest();
      const csrf_token = document.querySelector('#csrf').childNodes[0]['value'];
      request.open('POST', '/');
      request.setRequestHeader("X-CSRFToken", csrf_token);

      // Retrieve user input from the "Contact Us" form
      let name      = document.querySelector('#name').value;
      let address   = document.querySelector('#address').value;
      let phone_ac  = document.querySelector('#phone_ac').value;
      let phone_3d  = document.querySelector('#phone_3d').value;
      let phone_4d  = document.querySelector('#phone_4d').value;
      let phone     = phone_ac + phone_3d + phone_4d
      if (document.querySelector('#phone_ext').value !== '') {
        let phone_ext = document.querySelector('#phone_ext').value;
        phone += ' ext. ' + phone_ext;
      };
      let email     = document.querySelector('#email').value;
      let message   = document.querySelector('#message').value;

      // Ensure that the Name, Email Address, and Message fields are not empty in
      // the "Contact Us" form
      if (name !== '' && email !== '' && message !== '') {

        // Clear "Contact Us" form data after submission
        document.querySelector('#name').value = '';
        document.querySelector('#address').value = '';
        document.querySelector('#phone_ac').value = '';
        document.querySelector('#phone_3d').value = '';
        document.querySelector('#phone_4d').value = '';
        document.querySelector('#email').value = '';
        document.querySelector('#message').value = '';

        // Clear the error message and revert required field headers to default in
        // case the user had previously submitted an incomplete form
        document.querySelector('#alert').innerHTML = "";
        document.querySelector('#alert').className = "";
        required_fields = document.querySelectorAll('#required_field');
        for (let i = 0; i < required_fields.length; i++) {
          required_fields[i].style.color="black";
        };

        // Append user input to message_data (the FormData() object)
        const message_data = new FormData();
        message_data.append('name',       name);
        message_data.append('address',    address);
        message_data.append('phone',      phone);
        message_data.append('email',      email);
        message_data.append('message',    message);
        message_data.append('success',    true);

        // View the contents of FormData() in browser console
        // for (let i of message_data.entries()) {
        //   console.log(i);
        // };

        // Send a "Message successfully sent!" alert to the DOM in the event of a
        // successful "Contact Us" form submission
        document.querySelector('#alert').innerHTML = "Your message has been sent!";
        document.querySelector('#alert').className = "alert alert-success";

        // Send FormData() object to server
        request.send(message_data);
        return false;

      // Display error message and highlight required fields if any of them are
      // empty
      } else {
        document.querySelector('#alert').innerHTML = "Please fill in all required fields.";
        document.querySelector('#alert').className = "alert alert-danger";
        required_fields = document.querySelectorAll('#required_field');
        for (let i = 0; i < required_fields.length; i++) {
          required_fields[i].style.color="red";
        };
        return false;
      };
    } else {
      document.querySelector('#alert').innerHTML = "Please click the reCAPTCHA checkbox below.";
      document.querySelector('#alert').className = "alert alert-danger";
      return false;
    };
  };
});