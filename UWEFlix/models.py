from ctypes import addressof
from django.db import models
from django.contrib.auth.models import User


class Club(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    representative = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=300)
    landline = models.CharField(max_length=11)
    mobile = models.CharField(max_length=11)
    email = models.EmailField(max_length=30)
    
# Club models

class ClubAccount(models.Model):
    account_title = models.CharField(max_length=300)
    card_number = models.IntegerField()
    expiry_date = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.CASCADE)

# Cinema models
class Screen(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()

class Cinema(models.Model):
    name = models.CharField(max_length=300)
    screens = models.ForeignKey(Screen, on_delete=models.PROTECT)

class Film(models.Model):
    title = models.CharField(max_length=300)
    #rating = models.IntegerField(max_length=1)
    duration = models.IntegerField()
    short_description = models.CharField(max_length=300)
    long_description = models.CharField(max_length=300)
    image_URL = models.URLField()
    #trailer_url = models.URLField()
    upload_date = models.DateTimeField("date logged")

class Showing(models.Model):
    date = models.DateField()
    time = models.TimeField()
    film = models.ForeignKey(Film, on_delete=models.PROTECT)
    screen = models.ForeignKey(Screen, on_delete=models.PROTECT)

# Customer models

class Customer(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    card_number = models.IntegerField()
    expiry_date = models.DateField()

class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    showing = models.ForeignKey(Showing, on_delete=models.PROTECT)

class Ticket(models.Model):
    type = ["student", "child", "adult"]
    number = models.IntegerField()
    booking = models.ForeignKey(Booking, on_delete=models.PROTECT) 