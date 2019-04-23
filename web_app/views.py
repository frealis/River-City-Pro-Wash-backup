from botocore.exceptions import ClientError
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from string import Template
from urllib.parse import parse_qs
from web_app.models import Message

import bleach, boto3 json, os, urllib.request


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
    # RECAPTCHA_SITE_SECRET = os.getenv('RECAPTCHA_SITE_SECRET')    # heroku
    RECAPTCHA_SITE_SECRET = os.environ['RECAPTCHA_SITE_SECRET']   # aws

    # reCAPTCHA v2 SECRET key, test
    # RECAPTCHA_SITE_SECRET = '6LeIxAcTAAAAAGG-vFI1TnRWxMZNFuojJ4WifJWe'

    # a = os.getenv('RECAPTCHA_SITE_VERIFY_URL')    # heroku, local
    a = os.environ['RECAPTCHA_SITE_VERIFY_URL']     # aws

    b = urllib.parse.urlencode({'secret': RECAPTCHA_SITE_SECRET, 'response': request.POST['recaptcha']}, True)
    c = urllib.request.Request(a + '?' + b)
    recaptcha_response = urllib.request.urlopen(c).read().decode("utf-8")
    if json.loads(recaptcha_response).get("success") == True:
      recaptcha = 'Success'
      print('=== reCAPTCHA succeeded ===')

      # Save data submitted from the "Contact Us" form to database -- if there is
      # a problem with the database connection, then the rest of the code in 
      # this function will not execute (ie. mail will not be sent)
      m = Message(name=name, address=address, phone=phone, email=email, message=message, ip=ip, recaptcha=recaptcha)
      m.save()

      # Set email administrator address
      # email_admin = os.getenv('EMAIL_ADMIN')    # heroku, local
      email_admin = os.environ['EMAIL_ADMIN']   # aws

      SENDER = "Sender Name <rvaprowash@gmail.com>"
      RECIPIENT = "rvaprowash@gmail.com"
      AWS_REGION = "us-east-1"

      # The subject line for the email.
      SUBJECT = "Amazon SES Test (SDK for Python)"

      # The email body for recipients with non-HTML email clients.
      BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                  "This email was sent with Amazon SES using the "
                  "AWS SDK for Python (Boto)."
                  )
                  
      # The HTML body of the email.
      BODY_HTML = """<html>
      <head></head>
      <body>
        <h1>Amazon SES Test (SDK for Python)</h1>
        <p>This email was sent with
          <a href='https://aws.amazon.com/ses/'>Amazon SES</a> using the
          <a href='https://aws.amazon.com/sdk-for-python/'>
            AWS SDK for Python (Boto)</a>.</p>
      </body>
      </html>
                  """            

      # The character encoding for the email.
      CHARSET = "UTF-8"

      # Create a new SES resource and specify a region.
      client = boto3.client('ses',region_name=AWS_REGION)

      # Try to send the email.
      try:
          #Provide the contents of the email.
          response = client.send_email(
              Destination={
                  'ToAddresses': [
                      RECIPIENT,
                  ],
              },
              Message={
                  'Body': {
                      'Html': {
                          'Charset': CHARSET,
                          'Data': BODY_HTML,
                      },
                      'Text': {
                          'Charset': CHARSET,
                          'Data': BODY_TEXT,
                      },
                  },
                  'Subject': {
                      'Charset': CHARSET,
                      'Data': SUBJECT,
                  },
              },
              Source=SENDER,
          )
      # Display an error if something goes wrong.	
      except ClientError as e:
          print(e.response['Error']['Message'])
      else:
          print("Email sent! Message ID:"),
          print(response['MessageId'])

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
