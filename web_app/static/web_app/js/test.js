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

document.addEventListener('DOMContentLoaded', function() {

  // Retrieve message from "Contact Us" form and submit
  document.querySelector('#send_message').onclick = () => {

    // Initialize POST request, extract the CSRF value from the index.html DOM,
    // and put that into the header of the POST request
    const request = new XMLHttpRequest();
    const csrf_token = document.querySelector('#csrf').childNodes[0]['value'];
    request.open('POST', '/test');
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

    console.log('name: ', name, 'address: ', address, 'phone: ', phone, 'email: ', email, 'message: ', message);

    // Append user input to message_data (the FormData() object)
    const message_data = new FormData();
    message_data.append('name',       name);
    message_data.append('address',    address);
    message_data.append('phone',      phone);
    message_data.append('email',      email);
    message_data.append('message',    message);

    // View the contents of FormData() in browser console
    // for (let i of message_data.entries()) {
    //   console.log(i);
    // };

    // Send FormData() object to server
    request.send(message_data);
    return false;
  };
});

