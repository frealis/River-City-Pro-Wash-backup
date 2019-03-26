from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'web_app/index.html')

def test(request):
  if request.method == 'POST':
    name = request.POST['name']
    address = request.POST['address']
    phone = request.POST['phone']
    email = request.POST['email']
    message = request.POST['message']

    # print('name: ', name, 'address: ', address, 'phone: ', phone, 'email: ', email, 'message: ', message)

    from web_app.models import Message
    m = Message(name=name, address=address, phone=phone, email=email, message=message)
    m.save()

  return render(request, 'web_app/test.html')