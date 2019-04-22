from django.core.mail import send_mail
from string import Template

print('============ GMAIL =============')

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