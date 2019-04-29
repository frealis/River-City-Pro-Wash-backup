from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from string import Template
from urllib.parse import parse_qs
from web_app.models import Message

import bleach, json, os, urllib.request


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
    
    # reCAPTCHA v3 SECRET key
    # RECAPTCHA_SITE_SECRET = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'  # local
    RECAPTCHA_SITE_SECRET = os.getenv('RECAPTCHA_SITE_SECRET')    # heroku
    # RECAPTCHA_SITE_SECRET = os.environ['RECAPTCHA_SITE_SECRET']   # aws

    a = os.getenv('RECAPTCHA_SITE_VERIFY_URL')    # heroku, local
    # a = os.environ['RECAPTCHA_SITE_VERIFY_URL']     # aws

    b = urllib.parse.urlencode({'secret': RECAPTCHA_SITE_SECRET, 'response': request.POST['recaptcha']}, True)
    c = urllib.request.Request(a + '?' + b)
    recaptcha_response = urllib.request.urlopen(c).read().decode("utf-8")

    print('=================== recaptcha_response: ', recaptcha_response)
    if json.loads(recaptcha_response).get("success") == True:

      # Set recaptcha = 'Success' to be stored in database
      recaptcha = 'Success'
      print('=== reCAPTCHA succeeded ===')

      # Set email administrator address
      # email_admin = os.getenv('EMAIL_ADMIN')    # heroku, local
      # email_admin = os.environ['EMAIL_ADMIN']   # aws

      # === Email settings go here ===

      # Save data submitted from the "Contact Us" form to database -- if there is
      # a problem with the database connection, then the rest of the code in 
      # this function will not execute (ie. mail will not be sent)
      # m = Message(name=name, address=address, phone=phone, email=email, message=message, ip=ip, recaptcha=recaptcha)
      # m.save()


      # Just put this here to silence a server error message since it looks like
      # request.method == 'POST' requires some kind of HttpResponse object
      response = HttpResponse()
      response['blank_response'] = 'blank_response'
      return response

    else:

      # Set recaptcha = 'Fail' to be stored in database
      recaptcha = 'Fail'
      print('=== reCAPTCHA failed ===')

      # Save data submitted from the "Contact Us" form to database (reCAPTCHA
      # failed)
      # m = Message(name=name, address=address, phone=phone, email=email, message=message, ip=ip, recaptcha=recaptcha)
      # m.save()

      # Just put this here to silence a server error message since it looks like
      # request.method == 'POST' requires some kind of HttpResponse object
      response = HttpResponse()
      response['blank_response'] = 'blank_response'
      return response

  if request.method == 'GET':
    return render(request, 'web_app/index.html')

def xtest(request):
  return render(request, 'web_app/xtest.html')
