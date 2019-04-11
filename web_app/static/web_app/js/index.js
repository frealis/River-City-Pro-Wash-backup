// Restrict phone number field to numbers 0 through 9
function noLetters(event) {
  var keycode = event.which;
  if (keycode < 48 || keycode > 57) {
    return false;
  };
}

// Restrict phone number extention field to exclude spaces
function noSpaces(event) {
  var keycode = event.which;
  if (keycode === 32) {
    return false;
  };
}

// Toggle navbar fixed-top class
window.onscroll = () => {
  // console.log('----');
  // console.log('window.innerHeight: ', window.innerHeight);
  // console.log('window.scrollY: ', window.scrollY);
  // console.log('document.body.offsetHeight: ', document.body.offsetHeight);

  var navbar_offset = navbar.offsetTop;

  if (window.scrollY < navbar_offset) {
    document.querySelector('#nav_bar').classList.remove('fixed-top')
    document.querySelector('#nav_bar').classList.add('prevent_pushdown')

  } else if (window.scrollY >= navbar_offset) {
    document.querySelector('#nav_bar').classList.remove('prevent_pushdown')
    document.querySelector('#nav_bar').classList.add('fixed-top')
  };
}

document.addEventListener('DOMContentLoaded', function() {

  // Check to see if screen is resized on window load
  // Only collapse the navbar on a link click if the screen is less than 992px wide
  // https://www.sitepoint.com/javascript-media-queries/
  let mq = window.matchMedia( "(max-width: 992px)" );
  if (mq.matches) {
    document.querySelector('#navbarCollapse').setAttribute('data-toggle', 'collapse');
    document.querySelector('#navbarCollapse').setAttribute('data-target', '#navbarCollapse');
  } else {
    document.querySelector('#navbarCollapse').removeAttribute('data-toggle', 'collapse');
    document.querySelector('#navbarCollapse').removeAttribute('data-target', '#navbarCollapse');
  };

  // Re-check screen size with every window resize and change navbar if necessary.
  // There may be a way to combine the code directly above and below with in a
  // DO/WHILE loop, but since event listeners can't return anything I'm not sure
  // how.
  window.addEventListener("resize", function() {
    if (mq.matches) {
      document.querySelector('#navbarCollapse').setAttribute('data-toggle', 'collapse');
      document.querySelector('#navbarCollapse').setAttribute('data-target', '#navbarCollapse');
    } else {
      document.querySelector('#navbarCollapse').removeAttribute('data-toggle', 'collapse');
      document.querySelector('#navbarCollapse').removeAttribute('data-target', '#navbarCollapse');
    };
  });

  // Retrieve message from "Contact Us" form and submit
  document.querySelector('#send_message').onclick = () => {

    // console.log('grecaptcha.getResponse(): ', grecaptcha.getResponse())

    // Ensure that the reCAPTCHA v2 checkbox is ticked
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

        // Append user input & reCAPTCHA v2 token to message_data (the FormData() 
        // object)
        const message_data = new FormData();
        message_data.append('name',       name);
        message_data.append('address',    address);
        message_data.append('phone',      phone);
        message_data.append('email',      email);
        message_data.append('message',    message);
        message_data.append('recaptcha',  grecaptcha.getResponse());

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