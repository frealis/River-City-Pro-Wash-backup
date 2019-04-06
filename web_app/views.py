from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from string import Template
import bleach
import os

def index(request):
  if request.method == 'POST':

    # Gather & sanitize data submitted from the "Contact Us" form
    name = bleach.clean(request.POST['name'])
    address = bleach.clean(request.POST['address'])
    phone = bleach.clean(request.POST['phone'])
    email = bleach.clean(request.POST['email'])
    message = bleach.clean(request.POST['message'])

    # Save data submitted from the "Contact Us" form to database
    from web_app.models import Message
    m = Message(name=name, address=address, phone=phone, email=email, message=message)
    m.save()

    # Set the email address for the site administrator
    email_admin = os.getenv("EMAIL_ADMIN")

    # Send a notification message to the site administrator when "Contact Us" form
    # is submitted
    send_mail(
      'River City Pro Wash -- Contact Us form submission notification',
      Template('Name: $name\nAddress: $address\nPhone: $phone\nEmail: $email\nMessage: $message').substitute(name=name, address=address, phone=phone, email=email, message=message),
      email_admin,
      [email_admin],
      fail_silently=False,
    )

    # Send a thank you message to the user who submitted the "Contact Us" form
    send_mail(
      'Thank you for contacting River City Pro Wash!',
      Template('Dear $name,\n\nThank you for contacting River City Pro Wash! A member of our team will be in touch with you shortly.\n\nRegards,\nRiver City Pro Wash').substitute(name=name),
      email_admin,
      [email],
      fail_silently=False,
    )

  context = {
    'GOOGLE_MAPS_API_KEY': os.getenv('GOOGLE_MAPS_API_KEY')
  }

  # Change to REDIRECT
  return render(request, 'web_app/index.html', context)

def test(request):
  return render(request, 'web_app/test.html')
