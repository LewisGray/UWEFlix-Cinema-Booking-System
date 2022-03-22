from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import ListView
from UWEFlix.models import Film
from UWEFlix.forms import *
from math import *

# Class to provide film information for the home page
class StudentFilmListView(ListView):
    # Define the model to use as films
    model = Film
    # Overwrite the get context data function
    def get_context_data(self, **kwargs):
        # Set the number of films per row
        column_number = 3
        # Get the context
        context = super(StudentFilmListView, self).get_context_data(**kwargs)
        # Get the films through an SQL query
        film_list = Film.objects.order_by("-upload_date")
        # Define the film list, split into rows
        split_film_list = []
        # Calculate the number of rows
        row_number = ceil(len(film_list)/column_number)
        # For each row
        for row in range(row_number):
            # Get the start position of films to get from the film list
            start_pos = row * column_number
            # Get the end position of films to get from the film list
            end_pos = start_pos + column_number
            # If the end position is beyond the size of the film list 
            if end_pos > len(film_list):
                # Set the position to the size of the film list
                end_pos = len(film_list)
            # Add a list of films for the row on to the split film list
            split_film_list.append(Film.objects.order_by("-upload_date")[start_pos:end_pos])
        # Define the movies list in the context as the split film list
        context['movies_list'] = split_film_list
        # Return the context
        return context

# Student view presenting the UI to book tickets
def student_view(request):
    return render(request, "UWEFlix/student.html")

# About page view navigated from navbar
def about(request):
    return render(request, "UWEFlix/about.html")

# View to provide representative a UI to manage films
def movies(request):
    return render(request, "UWEFlix/movies.html")

# About page view navigated from navbar
def login(request):
    return render(request, "UWEFlix/login.html")

# View to provide cinema manager a UI to manage films
def cinema_management_view(request):
    return render(request, "UWEFlix/cinema_manager.html")

# View to provide account manager a UI to manage accounts
def account_management_view(request):
    return render(request, "UWEFlix/account_manager.html")

# View to provide representative a UI to manage films
def representative_view(request):
    return render(request, "UWEFlix/representative.html")

# Temporary to function to allow the addition of films to the database
def temp_log_film(request):
    # Define the form
    form = TempLogFilmForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the film is valid
        if form.is_valid():
            # Save the film details
            film = form.save(commit=False)
            film.upload_date = datetime.now()
            film.save()
            # Return the user to the homepage
            return redirect("home")
    # Otherwise
    else:
        # Take the user to the film creator page
        return render(request, "UWEFlix/temp_film_creator.html", {"form": form})