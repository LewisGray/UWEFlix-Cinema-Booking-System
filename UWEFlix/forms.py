from dataclasses import fields
from django import forms
from UWEFlix.models import Booking, Film
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# A form to add a film to the database
class LogFilmForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Set the model type to film
        model = Film
        # Define the fields to be included in the film
        fields = ("title", "short_description", "duration", "image_URL")

# A form to add a user to the database
class LogUserForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Set the model type to film
        model = User
        # Define the fields to be included in the film
        fields = ("username", "email")

# A form to add a user to the database
class LogBookingForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Set the model type to film
        model = Booking
        # Define the fields to be included in the film
        fields = ()

# A film to create a new user
class CreateUserForm(UserCreationForm):
    # metadata
    class Meta:
        # Using User models
        model = User
        # Get the username, email, password and checking password
        fields = ['username', 'email', 'password1', 'password2']

# A film to login the user
class LoginUserForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Using the User models
        model = User
        # Get the username and password
        fields = ['username', 'password']
        # Set the password as a password input to hide the text
        widgets = {'password': forms.PasswordInput()}