from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import ListView
from UWEFlix.models import Film
from UWEFlix.forms import *
from math import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.contrib.auth.models import Group
from django.contrib import messages
from UWEFlix.decorators import *


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

# The login page
@unauthenticated_required
def loginView(request):
    # Get the login from from forms.py
    form = LoginUserForm
    # If the form is being posted
    if request.method == "POST":
        # Get the username
        username = request.POST.get('username')
        # Get the password
        password = request.POST.get('password')
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        # If the user exists
        if user is not None:
            # Login the user
            login(request, user)
            # Direct the user to the home page
            return redirect('/')
        # otherwise
        else:
            # Alert the user the details are incorrect
            messages.info(request, 'Username or password is incorrect!')
    # Put the form into the context
    context = {'form': form}
    # Render the page with the context
    return render(request, "UWEFlix/login.html", context)

# Logout view
def userLogout(request):
    # Log the user out
    logout(request)
    # Redirect them to the home page
    return redirect('home')

# Provide a registration page
@unauthenticated_required
def register(request):
    # Get the default registration form
    form = CreateUserForm()
    # If the registration form is being posted
    if request.method == "POST":
        # Fill the form with the form data
        form = CreateUserForm(request.POST)
        # If the form is valid
        if form.is_valid():
            # Save the form as a user
            user = form.save()
            # Get the username from the form
            username = form.cleaned_data.get("username")
            # Set the user's group to student - the basic level account
            user.groups.add(Group.objects.get(name="Student"))
            # Post that the account was created successfully
            messages.success(request, 'Account ' + username + ' created successfully!')
            # Redirect the user to the login page
            return redirect('login')
    # Put the form into the context
    context = {'form': form}
    # Render the page with the context
    return render(request, "UWEFlix/register.html", context)

# View to provide cinema manager a UI to manage films
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def film_management_view(request):
    filmList = Film.objects.all()
    return render(request, "UWEFlix/film_manager.html",{'filmList':filmList})

# View to provide account manager a UI to manage accounts
def account_management_view(request):
    return render(request, "UWEFlix/account_manager.html")

# View to provide representative a UI to manage films
def representative_view(request):
    return render(request, "UWEFlix/representative.html")

# View to provide representative a UI to manage films
def noAccess(request):
    return render(request, "UWEFlix/no_access.html")

@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
# Function to allow the addition of films to the database
def log_film(request):
    # Define the form
    form = LogFilmForm(request.POST or None)
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
        return render(request, "UWEFlix/filmCRUD/film_form.html", {"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def updateFilm(request,filmName):
    film = Film.objects.get(title = filmName)
    form = LogFilmForm(instance=film)
  
    if request.method == "POST":
        # If the film is valid
        form = LogFilmForm(request.POST, instance = film)
        if form.is_valid():
           
            # Save the film details
            film = form.save(commit=False)
            film.upload_date = datetime.now()
            film.save()
            return redirect("home")
    return render(request, "UWEFlix/filmCRUD/film_form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def removeFilm(request,filmName):
    film = Film.objects.get(title = filmName )
    if request.method == "POST":
        film.delete()
        return redirect("home")
    return render(request, "UWEFlix/filmCRUD/remove_film.html",{"filmName": film.title})