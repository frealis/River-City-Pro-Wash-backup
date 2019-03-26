from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
  return render(request, 'web_app/index.html')

def test(request):
  if request.method == 'POST':
    name = request.POST['name']
    address = request.POST['address']
    phone = request.POST['phone_ac']
    email = request.POST['email']
    message = request.POST['message']


  return render(request, 'web_app/test.html')