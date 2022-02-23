from ctypes import addressof
from django.db import models

# Account models

class AccountManager(models.Model):
    username = models.CharField(max_length=300)
    password_hash = models.CharField(max_length=300)

class CinemaManager(models.Model):
    username = models.CharField(max_length=300)
    password_hash = models.CharField(max_length=300)

class RepresentativeAccount(models.Model):
    first_name = models.CharField(max_length=300)
    last_name = models.CharField(max_length=300)
    date_of_birth = models.DateField()
    username = models.CharField(max_length=300)
    password_hash = models.CharField(max_length=300)

# Club models

class ClubAccount(models.Model):
    account_title = models.CharField(max_length=300)
    card_number = models.IntegerField()
    expiry_date = models.DateField()

class Club(models.Model):
    name = models.CharField(max_length=300)
    representative = models.ForeignKey(RepresentativeAccount, on_delete=models.PROTECT)
    account = models.ForeignKey(ClubAccount, on_delete=models.PROTECT)
    address = models.CharField(max_length=300)
    landline = models.IntegerField()
    mobile = models.IntegerField()
    email = models.EmailField()

# Cinema models

class Screen(models.Model):
    number = models.IntegerField()
    capacity = models.IntegerField()

class Cinema(models.Model):
    name = models.CharField(max_length=300)
    screens = models.ForeignKey(Screen, on_delete=models.PROTECT)

class Film(models.Model):
    title = models.CharField(max_length=300)
    rating = models.CharField(max_length=300)
    duration = models.DurationField()
    description = models.CharField(max_length=300)
    image = models.URLField()
    trailer_url = models.URLField()

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