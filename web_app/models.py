from django.db import models

# Create your models here.
class Message(models.Model):
  name = models.CharField(max_length=64, default=None)
  address = models.CharField(max_length=200, default=None)
  phone = models.CharField(max_length = 32, default=None)
  email = models.CharField(max_length = 64, default=None)
  message = models.CharField(max_length = 800, default=None)
  created = models.DateTimeField(auto_now_add=True)
  ip = models.CharField(max_length = 64, default=None, blank=True, null=True)
  recaptcha = models.CharField(max_length = 64, default=None, blank=True, null=True)
  def __str__(self):
    return f"name: {self.name}, address: {self.address}, phone: {self.phone}, email: {self.email}, message: {self.message}, created: {self.created}, IP: {self.ip}, recaptcha: {self.recaptcha}"



    