from urllib import response
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import ListView
from UWEFlix.email import sendEmail
from UWEFlix.models import Film, Booking
from UWEFlix.forms import *
from math import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.contrib.auth.models import Group
from django.contrib import messages
from UWEFlix.decorators import *
from email import *


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


# View to provide cinema manager a UI to manage films
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def club_management_view(request):
    clubList = Club.objects.all()
    return render(request, "UWEFlix/club_manager.html",{'clubList':clubList})

# View to provide cinema manager a UI to manage user bookings
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def booking_management_view(request):
    #
    booking_list = Booking.objects.all()
    #
    return render(request, "UWEFlix/booking_management.html", {'booking_list': booking_list})

# View to allow a user to check their bookings
@login_required(login_url='login')
def user_bookings(request):
    #
    booking_list = Booking.objects.all()
    #
    return render(request, "UWEFlix/user_bookings.html", {'booking_list': booking_list})


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
        return render(request, "UWEFlix/filmCRUD/form.html", {"form": form})

#Update a film in the database
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
    return render(request, "UWEFlix/filmCRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def removeFilm(request,object):
    film = Film.objects.get(title = object )
    if request.method == "POST":
        film.delete()
        return redirect("home")
    return render(request, "UWEFlix/filmCRUD/remove_film.html",{"object": film.title})


#Remove a film from the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
# Function to allow the addition of clubss to the database
def log_club(request):
    # Define the form
    form = AddClubForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the club is valid
        if form.is_valid():
            # Save the club details
            club = form.save(commit=False)
            club.save()
            # Return the user to the homepage
            return redirect("home")
    # Otherwise
    else:
        # Take the user to the form page
        return render(request, "UWEFlix/filmCRUD/form.html", {"form": form})


@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def updateClub(request,clubName):
    club = Club.objects.get(name = clubName)
    form = AddClubForm(instance=club)
  
    if request.method == "POST":
        # If the club is valid
        form = AddClubForm(request.POST, instance = club)
        if form.is_valid():
           
            # Save the club details
            club = form.save(commit=False)
            club.save()
            return redirect("home")
    return render(request, "UWEFlix/filmCRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def removeClub(request,object):
    club = Club.objects.get(name = object)
    if request.method == "POST":
        club.delete()
        return redirect("home")
    return render(request, "UWEFlix/filmCRUD/remove_film.html",{"object": club.name})



# Log a booking
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def log_booking(request):
    # Define the form
    form = LogBookingForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the booking is valid
        if form.is_valid():
            # Save the booking details
            booking = form.save(commit=False)
            booking.upload_date = datetime.now()
            booking.save()
            #messages.success(request, 'Booking ' + booking.id + ' created successfully!')
            # Return the user to the homepage
            return redirect("home")
    # Otherwise
    else:
        # Take the user to the film creator page
        return render(request, "UWEFlix/bookingCRUD/booking_form.html", {"form": form})

# Update a booking
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def updateBooking(request, booking_id):
    # Get the booking object with a matching ID
    booking = Booking.objects.get(id = booking_id)
    # Get the booking form
    form = LogBookingForm(instance = booking)
    # If the form is being posted
    if request.method == "POST":
        # Get the user information from the user form
        form = LogBookingForm(request.POST, instance = booking)
        # If the film is valid
        if form.is_valid():
            # Save the film details
            booking = form.save(commit=False)
            booking.save()
            #messages.success(request, 'Details for ' + booking_id + ' updated successfully!')
            # Return to the booking management
            return redirect("booking_management")
    # Otherwise, return to the booking form
    return render(request, "UWEFlix/bookingCRUD/booking_form.html", {"form": form})

# Remove the booking
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def removeBooking(request, booking_id):
    # Get the booking with matching ID
    booking = Film.objects.get(id = booking_id)
    # If the form is being posted
    if request.method == "POST":
        # Delete the booking
        booking.delete()
        #messages.success(request, 'Booking ' + booking_id + ' deleted successfully!')
        # Return to the booking management page
        return redirect("booking_management")
    # Render the remove booking page
    return render(request, "UWEFlix/bookingCRUD/remove_film.html", {"object": booking.id})


# View to allow the cinema manager to manage the users
@login_required(login_url='login')
def user_management_view(request):
    # Get all the users
    user_list = User.objects.all()
    # Create a list to store roles
    roles = []
    # For each user
    for u in user_list:
        # For every group
        for group in u.groups.all():
            # Get the group name
            roles.append(group.name)
    # Package the users with the groups
    zipped_list = zip(user_list, roles)
    # Render the page with the users and groups
    return render(request, "UWEFlix/user_management.html", {'user_list': zipped_list})

# Log the user
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def log_user(request):
    # Define the form
    form = CreateUserForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the booking is valid
        if form.is_valid():
            # Save the booking details
            user = form.save(commit = False)
            user.save()
            # Set the user's group to student - the basic level account
            user.groups.add(Group.objects.get(name="Student"))
            # messages.success(request, 'Details for ' + user.username + ' created successfully!')
            # Return the user to the homepage
            return redirect("user_management")
    # Take the user to 
    return render(request, "UWEFlix/userCRUD/user_form.html", {"form": form, "creating": True})

# Update the user details
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def updateUser(request, username):
    # Get all the groups
    groups = Group.objects.all()
    # Get a user with the matching username
    user = User.objects.get(username = username)
    # Get the form
    form = LogUserForm(instance = user)
    # If the form is being posted
    if request.method == "POST":
        # If the password is being reset
        if "reset_password" in request.POST:
            # Establish a password
            password = "Password*1"
            # Set the user password
            user.password = password
            # messages.success(request, 'Password for ' + username + ' reset to ' + password + ' successfully!')
            # Return to the user amnagement page
            return redirect("user_management")
        # Otherwise
        else:
            # Get the form data
            form = LogUserForm(request.POST, instance = user)
            # If the film is valid
            if form.is_valid():
                # Save the film details
                user = form.save(commit=False)
                user.save()
                # Get the group from the dropdown
                selected_group = request.POST.get("selected_group")
                # For each group
                for group in groups:
                    # Remove the user from the group
                    group.user_set.remove(user)
                    # If the group matches the dropdown
                    if group.name == selected_group:
                        # Add the user to the group
                        group.user_set.add(user)
                # messages.success(request, 'Details for ' + username + ' updated successfully!')
                # Return to the user management page
                return redirect("user_management")
    # Get all the group names
    groups = Group.objects.all().values_list('name', flat=True)
    # Pass in the form data and the group names
    return render(request, "UWEFlix/userCRUD/user_form.html", {"form": form, "groups": groups})

# Remove the user from database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def removeUser(request, username):
    # Get the user from the username
    user = User.objects.get(username = username)
    # If the form is being posted
    if request.method == "POST":
        # Delete the user
        user.delete()
        # messages.success(request, 'Account ' + username + ' deleted successfully!')
        # Return to the user management page
        return redirect("user_management")
    # Go to the remove user page, passing in the username
    return render(request, "UWEFlix/userCRUD/remove_film.html", {"object": user.username})