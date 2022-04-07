from django.dispatch import receiver
from django.shortcuts import render
from django.contrib.auth.models import Group
from UWEFlix.models import Notification

# 
class TextItem():
    # 
    def __init__(self, text):
        # Get the text
        self.text = text

# Establish the navigation item class
class LinkItem():
    # Initiate the item
    def __init__(self, text, href):
        # Get the text
        self.text = text
        # Get the href link
        self.href = href

# 
class LinkDataItem():
    # 
    def __init__(self, text, href, data):
        # Get the text
        self.text = text
        # Get the href link
        self.href = href
        # Get the data for the item
        self.data = data

# Establish the navigation bar items
movie_nav_item = LinkItem("Movies", 'home')
about_nav_item = LinkItem("About", 'about')
login_nav_item = LinkItem("Login", 'login')
register_nav_item = LinkItem("Register", 'register')
bookings_nav_item = LinkItem("My Bookings", 'user_bookings')
account_nav_item = LinkItem("Accounts", 'account_management')
film_mgt_nav_item = LinkItem("Films", 'film_management')
booking_mgt_nav_item = LinkItem("Bookings", 'booking_management')
club_mgt_nav_item = LinkItem("Clubs", 'club_management')
user_mgt_nav_item = LinkItem("Users", 'user_management')
screen_mgt_nav_item = LinkItem("Screen", 'screens')
showing_mgt_nav_item = LinkItem("Showing", 'showing')

# Establish the header for each user type
group_nav_dictionary = {
    "None": [movie_nav_item, about_nav_item, login_nav_item, register_nav_item],
    "Student": [movie_nav_item, about_nav_item, bookings_nav_item],
    "Account Manager": [movie_nav_item, about_nav_item, account_nav_item, club_mgt_nav_item],
    "Club Representative": [movie_nav_item, about_nav_item, bookings_nav_item],
    "Cinema Employee": [movie_nav_item, about_nav_item, film_mgt_nav_item, showing_mgt_nav_item, screen_mgt_nav_item],
    "Cinema Manager": [movie_nav_item, about_nav_item, film_mgt_nav_item, booking_mgt_nav_item, club_mgt_nav_item, user_mgt_nav_item, showing_mgt_nav_item, screen_mgt_nav_item],
    "Admin": [movie_nav_item, about_nav_item, film_mgt_nav_item, booking_mgt_nav_item, account_nav_item, club_mgt_nav_item, user_mgt_nav_item, showing_mgt_nav_item, screen_mgt_nav_item]
}

# Establish the user information items
welcome_message_user_item = TextItem("Howdy, ")
logout_user_item = LinkItem("Logout", 'logout')
notifications_user_item = LinkDataItem("Notifications", 'notifications', 0)

# Set a dictionary for the user items
user_dictionary = {
    "None": [],
    "Student": [welcome_message_user_item, logout_user_item, notifications_user_item],
    "Account Manager": [welcome_message_user_item, logout_user_item, notifications_user_item],
    "Club Representative": [welcome_message_user_item, logout_user_item, notifications_user_item],
    "Cinema Employee": [welcome_message_user_item, logout_user_item, notifications_user_item],
    "Cinema Manager": [welcome_message_user_item, logout_user_item, notifications_user_item],
    "Admin": [welcome_message_user_item, logout_user_item, notifications_user_item]
}

# Get the user's group
def getGroup(user):
    # If the user doesn't belong to a group
    if len(user.groups.all()) == 0:
        # Return none
        return "None"
    # Otherwise return the user's group
    return user.groups.all()[0].name

# Get the number of notifications the user has
def getNotificationNumber(user):
    # Get the users unseen notifications
    notifications = Notification.objects.filter(receiver = user, seen = 0)
    # Return the number of notifications
    return len(notifications)

# Render the page with the user's navigation items
def dynamicRender(request, page, context = {}):
    # Get the user's group
    user_group = getGroup(request.user)
    # Get the navigation items for the user
    context["nav_items"] = group_nav_dictionary[user_group]
    # Get the user items
    context["user_items"] = user_dictionary[user_group]
    # If the user is logged in
    if not request.user.is_anonymous:
        # Add their name to the user item
        context["user_items"][0].text = f"Howdy, {request.user.username}!"
        # Set the user's number of notifications
        context["user_items"][2].data = getNotificationNumber(request.user)
    # Return the render of the page
    return render(request, page, context)