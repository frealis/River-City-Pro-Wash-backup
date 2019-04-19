from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from string import Template
from urllib.parse import parse_qs

import bleach
import json
import os
import urllib.request

# Index route (this is a single page web application, so everything is here)
def index(request):
  if request.method == 'POST':

    # Gather & sanitize data submitted from the "Contact Us" form
    name = bleach.clean(request.POST['name'])
    address = bleach.clean(request.POST['address'])
    phone = bleach.clean(request.POST['phone'])
    email = bleach.clean(request.POST['email'])
    message = bleach.clean(request.POST['message'])
    ip = request.META['REMOTE_ADDR']

    # Authenticate reCAPTCHA v2 user's response
    
    # reCAPTCHA v2 SECRET key
    RECAPTCHA_SITE_SECRET = os.getenv('RECAPTCHA_SITE_SECRET')

    # reCAPTCHA v2 SECRET key, test
    # RECAPTCHA_SITE_SECRET = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    a = os.getenv('RECAPTCHA_SITE_VERIFY_URL')
    b = urllib.parse.urlencode({'secret': RECAPTCHA_SITE_SECRET, 'response': request.POST['recaptcha']}, True)
    c = urllib.request.Request(a + '?' + b)
    recaptcha_response = urllib.request.urlopen(c).read().decode("utf-8")
    if json.loads(recaptcha_response).get("success") == True:
      recaptcha = 'Success'
      print('=== reCAPTCHA succeeded ===')

      # Save data submitted from the "Contact Us" form to database
      from web_app.models import Message
      m = Message(name=name, address=address, phone=phone, email=email, message=message, ip=ip, recaptcha=recaptcha)
      m.save()

      # Set the email address for the site administrator
      email_admin = os.getenv("EMAIL_ADMIN")

      # Send a notification message to the site administrator when "Contact Us" form
      # is submitted
      # send_mail(
      #   'River City Pro Wash -- Contact Us form submission notification',
      #   Template('Name: $name\nAddress: $address\nPhone: $phone\nEmail: $email\nMessage: $message').substitute(name=name, address=address, phone=phone, email=email, message=message),
      #   email_admin,
      #   [email_admin],
      #   fail_silently=False,
      # )

      # Use Gmail to send thank you email to client
      # send_mail(
      #   'Thank you for contacting River City Pro Wash!',
      #   Template('Dear $name,\n\nThank you for contacting River City Pro Wash! A member of our team will be in touch with you shortly.\n\nRegards,\nRiver City Pro Wash').substitute(name=name),
      #   email_admin,
      #   [email],
      #   fail_silently=False,
      # )

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

      # Just put this here to silence a server error message since it looks like
      # request.method == 'POST' requires some kind of HttpResponse object
      response = HttpResponse()
      response['blank_response'] = 'blank_response'
      return response

    else:
      recaptcha = 'Fail'
      print('=== reCAPTCHA failed ===')

      # Save data submitted from the "Contact Us" form to database (reCAPTCHA
      # failed)
      from web_app.models import Message
      m = Message(name=name, address=address, phone=phone, email=email, message=message, ip=ip, recaptcha=recaptcha)
      m.save()

      # Just put this here to silence a server error message since it looks like
      # request.method == 'POST' requires some kind of HttpResponse object
      response = HttpResponse()
      response['blank_response'] = 'blank_response'
      return response

  if request.method == 'GET':
    return render(request, 'web_app/index.html')

def xtest(request):
  return render(request, 'web_app/xtest.html')
