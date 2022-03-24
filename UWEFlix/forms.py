from django import forms
from UWEFlix.models import Film



class LogFilmForm(forms.ModelForm):
    # Metadata class
    class Meta:
        # Set the model type to film
        model = Film
        # Define the fields to be included in the film
        fields = ("title", "short_description", "duration", "image_URL")




