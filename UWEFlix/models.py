from ctypes import addressof
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver


class Club(models.Model):
    name = models.CharField(max_length=300, primary_key=True)
    representative = models.ForeignKey(User, on_delete=models.PROTECT)
    address = models.CharField(max_length=300)
    landline = models.CharField(max_length=11)
    mobile = models.CharField(max_length=11)
    email = models.EmailField(max_length=30)
    def __str__(self):
        return str(self.name)
    
# Club models

class ClubAccount(models.Model):
    account_title = models.CharField(max_length=300)
    card_number = models.IntegerField()
    expiry_date = models.DateField()
    club = models.ForeignKey(Club, on_delete=models.PROTECT)
    discountRate = models.FloatField(default = 0.00)
    balance = models.FloatField(default = 0.00)
    

# Cinema models
class Screens(models.Model):
    number = models.IntegerField() 
    capacity = models.IntegerField()
    def __str__(self):
        return str(self.number)


class Film(models.Model):
    title = models.CharField(max_length=300)
    #rating = models.IntegerField(max_length=1)
    duration = models.IntegerField()
    short_description = models.CharField(max_length=300)
    long_description = models.CharField(max_length=300)
    image_URL = models.URLField()
    #trailer_url = models.URLField()
    upload_date = models.DateTimeField("date logged")
    def __str__(self):
        return self.title
        

class Showing(models.Model):
    date = models.DateField()
    time = models.TimeField()
    film = models.ForeignKey(Film, on_delete=models.PROTECT)
    screen = models.ForeignKey(Screens, on_delete=models.PROTECT)
    taken_tickets = models.IntegerField()
    def __str__(self):
        return str(self.film)+" "+str(self.date)+" "+str(self.time)

# Customer models

class Customer(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField()
    card_number = models.IntegerField()
    expiry_date = models.DateField()

class Booking(models.Model):
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    showing = models.ForeignKey(Showing, on_delete=models.PROTECT)
    student_tickets = models.IntegerField()
    child_tickets = models.IntegerField()
    adult_tickets = models.IntegerField()
    cost = models.FloatField()

class Ticket(models.Model):
    ticketType = models.CharField(primary_key = True,max_length=20)
    ticketPrice = models.FloatField()

# Notifications

class Notification(models.Model):
    message = models.CharField(max_length=500)
    sent_date = models.DateTimeField("date logged")
    receiver = models.ForeignKey(User, on_delete=models.PROTECT)
    seen = models.BooleanField()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unseen_notifications = models.IntegerField()
