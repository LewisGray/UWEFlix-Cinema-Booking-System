from urllib import response
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import ListView
from UWEFlix.email import sendEmail
from UWEFlix.models import ClubAccount, Film, Booking, Notification, Showing, Screens, Ticket, tempBooking
from UWEFlix.forms import *
from django.contrib.auth import *
from django.contrib.auth.decorators import *
from django.contrib.auth.models import Group
from django.contrib import messages
from UWEFlix.decorators import *
from email import *
from django.contrib.auth.forms import PasswordChangeForm
from django.http import HttpResponseRedirect
from django.http import JsonResponse
import json
from UWEFlix.notifications import getNotifications, deleteNotification, sendNotificationToGroup, sendNotificationToUser
from UWEFlix.render import dynamicRender, getFilmContext, getTopBarContext, getGroup
import random
import string
from UWEFlix.widgets import getWidgets
from django.contrib.auth import views as auth_views

# Student view presenting the UI to book tickets
def student_view(request):
    # Get the films
    context = getFilmContext(3)
    # Get the user group
    group = getGroup(request.user)
    # Otherwise if they are the cinema manager
    if group == "Cinema Manager":
        # Take them to the cinema manager home
        return redirect('cinema_manager_home')
    # If they are a cinema employee
    elif group == "Cinema Employee":
        # Take them to the cinema employee home
        return redirect('cinema_employee_home')
    # Otherewise if it's the account manager
    elif group == "Account Manager":
        # Take them to the account manager home
        return redirect('account_manager_home')
    # Otherwise, render the student page
    return dynamicRender(request, "UWEFlix/student.html", context)

# Get the home page for the user type
def widgetHome(request):
    # Get the films
    context = getFilmContext(3)
    #
    context["widgets"] = getWidgets(getGroup(request.user))
    # Return the home page
    return dynamicRender(request, "UWEFlix/widget_home.html", context)

# About page view navigated from navbar
def about(request):
    return dynamicRender(request, "UWEFlix/about.html")

# View to provide representative a UI to manage films
def movies(request):
    return dynamicRender(request, "UWEFlix/movies.html")

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
    return dynamicRender(request, "UWEFlix/login.html", context)

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
    return dynamicRender(request, "UWEFlix/register.html", context)

# View to provide cinema manager a UI to manage films
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def film_management_view(request):
    filmList = Film.objects.all()
    return dynamicRender(request, "UWEFlix/film_manager.html",{'filmList':filmList})


# View to provide cinema manager a UI to manage films
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Account Manager"])
def club_management_view(request):
    clubList = Club.objects.all()
    return dynamicRender(request, "UWEFlix/club_manager.html",{'clubList':clubList})

# View to provide cinema manager a UI to manage user bookings
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def booking_management_view(request):
    #
    booking_list = Booking.objects.all()
    #
    return dynamicRender(request, "UWEFlix/booking_manager.html", {'booking_list': booking_list})

# View to allow a user to check their bookings
@login_required(login_url='login')
def user_bookings(request):
    # Get all the associated bookings for the user
    booking_list = Booking.objects.filter(customer=request.user)
    # Render the bookings page
    return dynamicRender(request, "UWEFlix/userBookings_manager.html", {'booking_list': booking_list})


# View to provide account manager a UI to manage accounts
def account_management_view(request):
    return dynamicRender(request, "UWEFlix/account_manager.html")

# View to provide representative a UI to manage films
def representative_view(request):
    return dynamicRender(request, "UWEFlix/representative.html")

# View to provide representative a UI to manage films
def noAccess(request):
    return dynamicRender(request, "UWEFlix/no_access.html")

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
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
            return redirect("film_management")
    # Otherwise
    else:
        # Take the user to the film creator page
        return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

#Update a film in the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def updateFilm(request, filmName):
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
            return redirect("film_management")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def removeFilm(request,object):
    film = Film.objects.get(title = object)
    if request.method == "POST":
        # Get all the showings
        showings = Showing.objects.all()
        # Is the film currently showing?
        current_showing = False
        # For each showing
        for showing in showings:
            # If the showing's film is the film to delete
            if showing.film == film:
                # Mark the film as currently showing
                current_showing = True
                # Break the loop
                break
        # If the film isn't currently showing
        if current_showing == False:
            # Delete the film from the database
            film.delete()
        return redirect("film_management")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": film.title})


#Remove a film from the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Account Manager"])
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
            return redirect("club_management")
    # Otherwise
    else:
        # Take the user to the form page
        return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})


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
            return redirect("club_management")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def removeClub(request,object):
    club = Club.objects.get(name = object)
    if request.method == "POST":
        club.delete()
        return redirect("club_management")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": club.name})


# Log a booking
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
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
            booking.time_booked = datetime.now()
            adultNum = int(request.POST.get('adult_tickets'))
            studentNum =int(request.POST.get('student_tickets'))
            childNum =int(request.POST.get('child_tickets'))
            adultTicket = Ticket.objects.get(ticketType = 'adult_ticket')
            studentTicket = Ticket.objects.get(ticketType = 'student_ticket')
            childTicket = Ticket.objects.get(ticketType = 'child_ticket')
            totalPrice = (adultTicket.ticketPrice*adultNum)+(studentTicket.ticketPrice*studentNum)+(childTicket.ticketPrice*childNum)
            booking.cost = totalPrice
            booking.save()
            #messages.success(request, 'Booking ' + booking.id + ' created successfully!')
            # Return the user to the homepage
            return redirect("booking_management")
    # Otherwise
    else:
        # Take the user to the film creator page
        return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

# Update a booking
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
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
            adultNum = int(request.POST.get('adult_tickets'))
            studentNum =int(request.POST.get('student_tickets'))
            childNum =int(request.POST.get('child_tickets'))
            adultTicket = Ticket.objects.get(ticketType = 'adult_ticket')
            studentTicket = Ticket.objects.get(ticketType = 'student_ticket')
            childTicket = Ticket.objects.get(ticketType = 'child_ticket')
            totalPrice = (adultTicket.ticketPrice*adultNum)+(studentTicket.ticketPrice*studentNum)+(childTicket.ticketPrice*childNum)
            booking.cost = totalPrice
            booking.save()
            #messages.success(request, 'Details for ' + booking_id + ' updated successfully!')
            # Return to the booking management
            return redirect("booking_management")
    # Otherwise, return to the booking form
    return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

# Remove the booking
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def removeBooking(request, booking_id):
    # Get the booking with matching ID
    booking = Booking.objects.get(id = booking_id)
    #
    next = request.POST.get('next', '/')
    # If the form is being posted
    if request.method == "POST":
        # Notify the customer their film has been cancelled
        sendNotificationToUser(request.user, booking.customer, f"Your booking for {booking.showing.film.title} at {booking.showing.date} has been cancelled.")
        #
        ticket_number = booking.student_tickets + booking.child_tickets + booking.adult_tickets
        #
        booking.showing.taken_tickets -= ticket_number
        # Delete the booking
        booking.delete()
        # Delete any notifications for the booking
        deleteNotification('remove_booking', str(booking_id))
        #messages.success(request, 'Booking ' + booking_id + ' deleted successfully!')
        # Return to the booking management page
        return HttpResponseRedirect(next)
    # Render the remove booking page
    return dynamicRender(request, "UWEFlix/CRUD/remove.html", {"object": booking.id})


# View to allow the cinema manager to manage the users
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def user_management_view(request):
    # Get all the users
    user_list = User.objects.all()
    # Create a list to store roles
    roles = []
    # For each user
    for u in user_list:
        # Add the role
        roles.append(getGroup(u))
    # Package the users with the groups
    zipped_list = zip(user_list, roles)
    # Render the page with the users and groups
    return dynamicRender(request, "UWEFlix/user_manager.html", {'user_list': zipped_list})

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
    return dynamicRender(request, "UWEFlix/userCRUD/form.html", {"form": form, "creating": True})

# Update the user details
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def updateUser(request, username):
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
            user.set_password(password)
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
                # Get all the groups
                groups = Group.objects.all()
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
    return dynamicRender(request, "UWEFlix/userCRUD/form.html", {"form": form, "groups": groups})

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
    return dynamicRender(request, "UWEFlix/CRUD/remove.html", {"object": user.username})

# Update own account details
@login_required(login_url='login')
def accountView(request):
    #
    user = request.user
    #
    password_form = PasswordChangeForm(request.user)
    #
    update_form = UpdateAccountForm(instance = user)
    #
    if request.method == "POST":
        #
        if "update_account" in request.POST:
            #
            update_form = UpdateAccountForm(request.POST, instance = user)
            # If the form is valid
            if update_form.is_valid():           
                # Save the club details
                user = update_form.save(commit = False)
                user.save()
                #
                return redirect("home")
        #
        else:
            #
            password_form = PasswordChangeForm(request.user, request.POST)
            # If the form is valid
            if password_form.is_valid():    
                #       
                user = password_form.save()
                #
                update_session_auth_hash(request, user)
                #
                #messages.success(request, 'Your password was successfully updated!')
                #
                return redirect('home')
            else:
                messages.error(request, 'Please correct the error below.')
    #
    return dynamicRender(request, "UWEFlix/account.html", {"update_form": update_form, "password_form": password_form})


# View to provide account manager a UI to manage club accounts
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Account Manager"])
def account_management_view(request):
    # Get a list of all the accounts
    account_list = ClubAccount.objects.all()
    # Return the account manager page with a list of accounts
    return dynamicRender(request, "UWEFlix/account_manager.html", {'account_list': account_list})

# Log a club account
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Account Manager"])
def log_account(request):
    # Define the form
    form = LogAccountForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the account is valid
        if form.is_valid():
            # Save the account details
            booking = form.save(commit=False)
            booking.save()
            #messages.success(request, 'Booking ' + booking.id + ' created successfully!')
            # Return the user to the homepage
            return redirect("account_management")
   
    return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

# Update an account
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Account Manager"])
def updateAccount(request, account_id):
    # Get the account object with a matching ID
    account = ClubAccount.objects.get(id = account_id)
    # Get the account form
    form = LogAccountForm(instance = account)
    # If the form is being posted
    if request.method == "POST":
        # Get the account information
        form = LogAccountForm(request.POST, instance = account)
        # If the account is valid
        if form.is_valid():
            # Save the account details
            account = form.save(commit=False)
            account.save()
            #messages.success(request, 'Details for ' + booking_id + ' updated successfully!')
            # Return to the account management
            return redirect("account_management")
    # Otherwise, return to the account form
    return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

# Remove the account
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Account Manager"])
def removeAccount(request, account_id):
    # Get the account with matching ID
    account = ClubAccount.objects.get(id = account_id)
    # If the form is being posted
    if request.method == "POST":
        # Delete the account
        account.delete()
        #messages.success(request, 'Booking ' + booking_id + ' deleted successfully!')
        # Return to the booking management page
        return redirect("account_management")
    # Render the remove booking page
    return dynamicRender(request, "UWEFlix/CRUD/remove.html", {"object": account.id})
    
    
    #Showings 

def showing_view(request):
    showingList = Showing.objects.all()
    return dynamicRender(request, "UWEFlix/showings.html", {'showingList':showingList})
    
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
# Function to allow the addition of showings to the database
def log_showing(request):
    # Define the form
    form = LogShowingForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the showings is valid
        if form.is_valid():
            # Save the film details
            showing = form.save(commit=False)
            showing.upload_date = datetime.now()
            showing.save()
            # Return the user to the homepage
            return redirect("showing")
    return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

#Update showings in the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def updateShowings(request, object):
    showingName = Showing.objects.get(id = object )
    form = LogShowingForm(instance=showingName)
    if request.method == "POST":
        # If the film is valid
        form = LogShowingForm(request.POST, instance = showingName)
        if form.is_valid():
            # Save the film details
            showingName = form.save(commit=False)
            showingName.save()
            return redirect("showing")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def removeShowings(request,object):
    showingName = Showing.objects.get(id = object)
    if request.method == "POST":
        showingName.delete()
        return redirect("showing")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": showingName.id})

#Screens 

def screen_view(request):
    screenList = Screens.objects.all()
    return dynamicRender(request, "UWEFlix/screens.html", {'screenList':screenList})
    
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
# Function to allow the addition of screens to the database
def log_screens(request):
    # Define the form
    form = LogScreenForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the screens is valid
        if form.is_valid():
            # Save the film details
            screens = form.save(commit=False)
            screens.save()
            # Return the user to the homepage
            return redirect("screens")
    # Otherwise
    else:
        # Take the user to the film creator page
        return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

#Update screens in the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def updateScreens(request, object):
    screenName = Screens.objects.get(id = object )
    
    form = LogScreenForm(instance=screenName)
  
    if request.method == "POST":
        # If the film is valid
        form = LogScreenForm(request.POST, instance = screenName)
        if form.is_valid():
           
            # Save the film details
            screenName = form.save(commit=False)
            screenName.save()
            return redirect("screens")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def removeScreens(request,object):
    screenName = Screens.objects.get(id = object)
    if request.method == "POST":
        screenName.delete()
        return redirect("screens")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": screenName.id})


# Book a film
@login_required(login_url='login')
def bookFilm(request, title):
    # Get the film object
    film_object = Film.objects.get(title = title)
    # Try
    try:
        # Get the showing list
        showing_list = Showing.objects.filter(film = film_object).order_by('date')
        current_date = None
        showing_list_date_seperated = []
        tempTest = []

        for showing in showing_list:
            if current_date != showing.date:
                tempTest = []
                tempTest.append(showing.date)
                tempTest.append([])
                tempTest[1].append(showing)
                current_date = showing.date
            else: 
                tempTest[1].append(showing)
            tempTest = []
            
            showing_list_date_seperated.append(tempTest)
        # print(showing_list)
        print('NEW SHOWING LIST!: ', showing_list_date_seperated)

    # If there are no showings
    except Showing.DoesNotExist:
        # Return home
        return redirect('home')
    # Otherwise render the userBookFilm, passing in the film title
    return dynamicRender(request, "UWEFlix/userBookFilm_manager.html", {'showing_list':showing_list_date_seperated, 'filmTitle': title})


#Book tickets
@login_required(login_url='login')
def bookTickets(request, showing_id):
    # Get the showing with matching ID
    showing = Showing.objects.get(id = showing_id)
    ##############################################
    #Alternate path for club reps to book
    if request.user.groups.filter(name = "Club Representative").exists():
        form = BookRepTicketsForm(request.POST or None)
        # If posting
        if request.method == "POST":
            # If the account is valid
            if form.is_valid():
                # Save the details
                booking = form.save(commit=False)
                booking.showing = showing
                booking.customer = request.user
                booking.child_tickets = 0
                booking.adult_tickets = 0
                # get the number of each type of ticket
                studentNum =int(request.POST.get('student_tickets'))
                ticket_number = studentNum
                #
                if ticket_number > booking.showing.screen.capacity - booking.showing.taken_tickets:
                    #
                    return HttpResponseRedirect(request.path_info)
                #Calculate cost and proceed to checkout  
                studentTicket = Ticket.objects.get(ticketType = 'student_ticket')
                clubRep = ClubRepresentative.objects.get(representative = request.user)
                club = Club.objects.get(representative = clubRep)
                clubAccount = ClubAccount.objects.get(club = club)
                totalPrice = (studentTicket.ticketPrice*studentNum)-((studentTicket.ticketPrice*studentNum)*clubAccount.discountRate)
                booking.cost = round(totalPrice,2)
                booking.save()
                #booking.showing.save()
                return dynamicRender(request, "UWEFlix/clubRepCheckout.html", {"booking": booking,"account":clubAccount})
                # Save the models
                #messages.success(request, 'Booking ' + booking.id + ' created successfully!')
        else:
            # Take the user to the film creator page
            return dynamicRender(request, "UWEFlix/CRUD/ticket_form.html", {"form": form})

#######################################################################################################
    else:
        # Define the form
        form = BookTicketsForm(request.POST or None)
        # If posting
        if request.method == "POST":
            # If the account is valid
            if form.is_valid():
                # Save the details
                booking = form.save(commit=False)
                booking.showing = showing
                booking.customer = request.user
                # get the number of each type of ticket
                adultNum = int(request.POST.get('adult_tickets'))
                studentNum =int(request.POST.get('student_tickets'))
                childNum =int(request.POST.get('child_tickets'))
                ticket_number = adultNum +studentNum+childNum
                #
                if ticket_number > booking.showing.screen.capacity - booking.showing.taken_tickets:
                    #
                    return HttpResponseRedirect(request.path_info)
                #Calculate cost and proceed to checkout
                adultTicket = Ticket.objects.get(ticketType = 'adult_ticket')
                studentTicket = Ticket.objects.get(ticketType = 'student_ticket')
                childTicket = Ticket.objects.get(ticketType = 'child_ticket')
                totalPrice = (adultTicket.ticketPrice*adultNum)+(studentTicket.ticketPrice*studentNum)+(childTicket.ticketPrice*childNum)
                booking.cost = totalPrice
                booking.save()
                #booking.showing.save()
                return dynamicRender(request, "UWEFlix/checkoutBooking.html", {"booking": booking, "cost":booking.cost})
                # Save the models
                
                #messages.success(request, 'Booking ' + booking.id + ' created successfully!')
        else:
            # Take the user to the film creator page
            return dynamicRender(request, "UWEFlix/CRUD/ticket_form.html", {"form": form})

#paypal booking complete 
@login_required(login_url='login')
def booking_complete(request):
    if request.method == "POST":
        body = json.loads(request.body)
        booking = tempBooking.objects.get(id = body['bookingID'])
        booking.showing.taken_tickets += (booking.student_tickets+booking.child_tickets+booking.adult_tickets)
        confirmedBooking = Booking(
            customer = booking.customer,
            showing = booking.showing,
            student_tickets = booking.student_tickets,
            child_tickets = booking.child_tickets,
            adult_tickets = booking.adult_tickets,
            time_booked = datetime.now(),
            cost = booking.cost )
        booking.paid = True
        booking.save()
        booking.showing.save()
        confirmedBooking.save()
         
    return JsonResponse('Payment submitted..', safe=False)

#complete page
@login_required(login_url='login')
def booking_success(request):
    return dynamicRender(request, "UWEFlix/complete_booking.html")



@login_required(login_url='login')
def club_booking_complete(request,Bid,Aid):
        booking = tempBooking.objects.get(id = Bid)
        clubAccount = ClubAccount.objects.get(id = Aid)
        booking.showing.taken_tickets += (booking.student_tickets+booking.child_tickets+booking.adult_tickets)
        confirmedBooking = Booking(
            customer = booking.customer,
            showing = booking.showing,
            student_tickets = booking.student_tickets,
            child_tickets = booking.child_tickets,
            adult_tickets = booking.adult_tickets,
            cost = booking.cost,
            time_booked = datetime.now() )
            
        clubAccount.balance += confirmedBooking.cost
        clubAccount.save()
        booking.save()
        booking.showing.save()
        confirmedBooking.save()
        return redirect("success")


        


# View a user's notifications
@login_required(login_url='login')
def viewNotifications(request):
    # Get the notifications list for the user
    notification_list = getNotifications(request.user)
    # If posting
    if request.method == "POST":
        # For each notification
        for notification in notification_list:
            # If it's ID is in the post (it has been selected to be deleted)
            if str(notification.id) in request.POST:
                # Delete the notification
                notification.delete()
                # Break the loop
                break
        # Return to the notifications page
        return redirect("notifications")
    # Get all the notifications for the user
    notifications = Notification.objects.filter(receiver = request.user).order_by('sent_date').reverse()
    # For each notification
    for notification in notifications:
        # If it's unseen
        if notification.seen == 0:
            # mark it as seen
            notification.seen = 1
            # Save the notification
            notification.save()
        # If it was seen last time
        elif notification.seen == 1:
            # Set the notification to seen
            notification.seen = 2
            # Save the notification
            notification.save()
    # Render the notification page using the notification list
    return dynamicRender(request, "UWEFlix/notification_manager.html", {'notification_list': notification_list})

# View a user's bookings
@login_required(login_url='login')
def user_bookings(request):
    # Get the user's bookings
    booking_list = Booking.objects.filter(customer = request.user)
    # If posting
    if request.method == "POST":
        # For each booking
        for booking in booking_list:
            # If it's ID is in the post (it has been selected to be deleted)
            if str(booking.id) in request.POST:
                # Send a notification to the cinema manager
                sendNotificationToGroup(request.user, "Cinema Manager", f"Request from {request.user.username} to delete booking {booking.id}", 'remove_booking', str(booking.id))
                # Break the loop
                break
        # Return to the bookings page
        return redirect("user_bookings")
    # Render the notification page using the notification list
    return dynamicRender(request, "UWEFlix/userBookings_manager.html", {'booking_list': booking_list})

    ########################################################################################################







# View to provide cinema manager a UI to manage films
@login_required(login_url='login')
@permitted(roles=["Cinema Manager"])
def clubRepresentative_management_view(request):
    repList = ClubRepresentative.objects.all()
    return dynamicRender(request, "UWEFlix/clubRep_manager.html",{'clubRep_list':repList})



@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
# Function to allow the addition of clubReps to the database
def log_clubRepresentative(request):
    # Define the form
    form = LogClubRepresentativeForm(request.POST or None)
    # If posting
    if request.method == "POST":
        # If the form is valid
        if form.is_valid():
            password = ''.join(random.choices(string.ascii_lowercase, k=10))
            clubRep = form.save(commit=False)
            clubRep.save()
            #Create a new user to allow the rep to login using their rep number and password
            clubRepUser = User(
                username = str(clubRep.clubRepNumber),
            )

            clubRepUser.set_password(password)
            clubRepUser.save()
            # Set the user's group to club rep - the basic level account
            clubRepUser.groups.add(Group.objects.get(name="Club Representative"))
            clubRep.representative = clubRepUser
            clubRep.clubRepPassword = password
            clubRep.save()
            # Return the user to the homepage
            return redirect("clubRepresentative_management")
    # Otherwise
    else:
        # Take the user to the clubRep creator page
        return dynamicRender(request, "UWEFlix/CRUD/form.html", {"form": form})

#Update screens in the database
@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def updateClubRepresentative(request, object):
    clubRep = ClubRepresentative.objects.get(clubRepNumber = object )
    
    form = LogClubRepresentativeForm(instance=clubRep)
  
    if request.method == "POST":
        # If the film is valid
        form = LogClubRepresentativeForm(request.POST, instance = clubRep)
        if form.is_valid():
           
            # Save the film details
            clubRep = form.save(commit=False)
            clubRep.save()
            return redirect("clubRepresentative_management")
    return dynamicRender(request, "UWEFlix/CRUD/form.html",{"form": form})

@login_required(login_url='login')
@permitted(roles=["Cinema Manager", "Cinema Employee"])
def removeClubRepresentative(request,object):
    clubRep = ClubRepresentative.objects.get(clubRepNumber = object)
    if request.method == "POST":
        clubRep.delete()
        return redirect("clubRepresentative_management")
    return dynamicRender(request, "UWEFlix/CRUD/remove.html",{"object": clubRep.clubRepNumber})


def settleAccount(request):
    clubRep = ClubRepresentative.objects.get(representative = request.user)
    club = Club.objects.get(representative = clubRep)
    clubAccount = ClubAccount.objects.get(club = club,)
    clubBookingList = Booking.objects.filter(customer = request.user)
    return dynamicRender(request, "UWEFlix/checkoutAccountSettlement.html",{"clubAccount": clubAccount,"clubBookingList": clubBookingList,"cost":clubAccount.balance})

def settle(request):
    if request.method == "POST":
        body = json.loads(request.body)
        clubAccount = ClubAccount.objects.get(id = body['accountID'])
        clubAccount.balance = 0
        clubAccount.save()
         
    return JsonResponse('Payment submitted..', safe=False)