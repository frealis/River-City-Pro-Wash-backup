# This is just a collection of code for different email services, not meant to
# run.

# Use Gmail to send a notification message to the site administrator when 
# "Contact Us" form is submitted
send_mail(
  'River City Pro Wash -- Contact Us form submission notification',
  Template('Name: $name\nAddress: $address\nPhone: $phone\nEmail: $email\nMessage: $message').substitute(name=name, address=address, phone=phone, email=email, message=message),
  email_admin,
  [email_admin],
  fail_silently=False,
)

# Use Gmail to send thank you email to client
send_mail(
  'Thank you for contacting River City Pro Wash!',
  Template('Dear $name,\n\nThank you for contacting River City Pro Wash! A member of our team will be in touch with you shortly.\n\nRegards,\nRiver City Pro Wash').substitute(name=name),
  email_admin,
  [email],
  fail_silently=False,
)

# Use SendGrid to send notification to site administrator
message = Mail(
  from_email=email_admin,
  to_emails=email_admin,
  subject='River City Pro Wash Contact Form Submission',
  html_content=Template('Name: $name<br>Address: $address<br>Phone: $phone<br>Email: $email<br>Message: $message').substitute(name=name, address=address, phone=phone, email=email, message=message))
try:
  sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
  response = sg.send(message)
except Exception as e:
  print('=========== SendGrid exception: ', e)

# Use SendGrid to send thank you email to client
message = Mail(
  from_email=email_admin,
  to_emails=email,
  subject='Thank you for contacting River City Pro Wash!',
  html_content=Template('Dear $name,<br><br>Thank you for contacting River City Pro Wash! A member of our team will be in touch with you shortly.<br><br>Regards,<br>River City Pro Wash<br><br>').substitute(name=name))
try:
  sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
  response = sg.send(message)
except Exception as e:
  print('=========== SendGrid exception: ', e)