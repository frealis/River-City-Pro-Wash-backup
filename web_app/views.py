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
    # RECAPTCHA_SITE_SECRET = os.getenv('RECAPTCHA_SITE_SECRET')    # heroku
    RECAPTCHA_SITE_SECRET = os.environ['RECAPTCHA_SITE_SECRET']   # aws

    # a = os.getenv('RECAPTCHA_SITE_VERIFY_URL')    # heroku, local
    a = os.environ['RECAPTCHA_SITE_VERIFY_URL']     # aws

    b = urllib.parse.urlencode({'secret': RECAPTCHA_SITE_SECRET, 'response': request.POST['recaptcha_token']}, True)
    c = urllib.request.Request(a + '?' + b)
    recaptcha_response = urllib.request.urlopen(c).read().decode("utf-8")

    print('=================== recaptcha_response: ', recaptcha_response)
    if json.loads(recaptcha_response).get("success") == True:
      recaptcha = 'Success'
      print('=== reCAPTCHA succeeded ===')

      # Set email administrator address
      # email_admin = os.getenv('EMAIL_ADMIN')    # heroku, local
      email_admin = os.environ['EMAIL_ADMIN']   # aws

      from botocore.exceptions import ClientError
      import boto3

      SENDER = Template("River City Pro Wash <$email_admin>").substitute(email_admin=email_admin)
      RECIPIENT = Template("$email").substitute(email=email)
      AWS_REGION = "us-east-1"

      # The subject line for the email.
      SUBJECT = "Thank you for contacting River City Pro Wash!"

      # The subject line for the site administrator.
      ADMIN_SUBJECT = "Contact Us Form Submission Notification"

      # The email body for recipients with non-HTML email clients.
      BODY_TEXT = (Template("Dear $name\r\n\n"
                  "Thank you for contacting River City Pro Wash! "
                  "A member of our team will contact you shortly.\n\n"
                  "Regards,\n"
                  "River City Pro Wash\n\n"
                  "(804) 239-6085\n"
                  "www.rivercityprowash.com").substitute(name=name)
                  )

      # The email body for administrators with non-HTML email clients.
      ADMIN_BODY_TEXT = (Template("Name: $name\n"
                  "Address: $address\n"
                  "Phone: $phone\n"
                  "Email: $email\n"
                  "Message: $message").substitute(name=name, address=address, phone=phone, email=email, message=message)
                  )
            
      # The HTML body of the email sent to the customer.
      BODY_HTML = """<html>
      <head></head>
      <body>
        <p>
          Dear """ + Template('$name').substitute(name=name) + """<br><br>
          Thank you for contacting River City Pro Wash!
          A member of our team will contact you shortly.<br><br>
          Regards,<br>
          River City Pro Wash<br><br>
          (804) 239-6085<br>
          www.rivercityprowash.com
        </p>
      </body>
      </html>
                  """

      phone_str = str(phone)
      phone_list = list(phone_str)
      phone_ac = phone_list[0] + phone_list[1] + phone_list[2]
      phone_3d = phone_list[3] + phone_list[4] + phone_list[5]
      phone_4d = phone_list[6] + phone_list[7] + phone_list[8] + phone_list[9]
      phone_pretty = Template('($phone_ac) $phone_3d - $phone_4d').substitute(phone_ac=phone_ac, phone_3d=phone_3d, phone_4d=phone_4d)

      # The HTML body of the email sent to the site administrator.
      ADMIN_BODY_HTML = """<html>
      <head></head>
      <body>
        <p>
          Name: """ + Template('$name').substitute(name=name) + """<br>
          Address: """ + Template('$address').substitute(address=address) + """<br>
          Phone: """ + Template('$phone').substitute(phone=phone_pretty) + """<br>
          Email: """ + Template('$email').substitute(email=email) + """<br>
          Message: """ + Template('$message').substitute(message=message) + """<br>
        </p>
      </body>
      </html>
                        """    

      # The character encoding for the email.
      CHARSET = "UTF-8"

      # Create a new SES resource and specify a region.
      client = boto3.client('ses',region_name=AWS_REGION)

      # Try to send the email.
      try:

        # Send thank-you email to customer.
        response = client.send_email(
          Destination={
            'ToAddresses': [RECIPIENT,],
          },
          Message={
            'Body': {
              'Html': {'Charset': CHARSET, 'Data': BODY_HTML,},
              'Text': {'Charset': CHARSET, 'Data': BODY_TEXT,},
            },
            'Subject': {'Charset': CHARSET, 'Data': SUBJECT,},
          },
          Source=SENDER,
        )

        # Send notification to site administrator when 'Contact Us' form is
        # submitted.
        response = client.send_email(
          Destination={
            'ToAddresses': [SENDER,],
          },
          Message={
            'Body': {
              'Html': {'Charset': CHARSET, 'Data': ADMIN_BODY_HTML,},
              'Text': {'Charset': CHARSET, 'Data': ADMIN_BODY_TEXT,},
            },
            'Subject': {'Charset': CHARSET, 'Data': ADMIN_SUBJECT,},
          },
          Source=SENDER,
        )

      # Display an error if something goes wrong.	
      except ClientError as e:
        print(e.response['Error']['Message'])
      else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

      # Save data submitted from the "Contact Us" form to database -- if there is
      # a problem with the database connection, then the rest of the code in 
      # this function will not execute (ie. mail will not be sent)
      m = Message(name=name, address=address, phone=phone, email=email, message=message, ip=ip, recaptcha=recaptcha)
      m.save()


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
