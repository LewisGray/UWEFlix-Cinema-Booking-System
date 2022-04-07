from django.shortcuts import render
from django.contrib.auth.models import Group

# Establish the navigation item class
class NavItem():
    # Initiate the item
    def __init__(self, text, href):
        # Get the text
        self.text = text
        # Get the href link
        self.href = href

# Establish the navigation bar items
movie_nav_item = NavItem("Movies", 'home')
about_nav_item = NavItem("About", 'about')
login_nav_item = NavItem("Login", 'login')
register_nav_item = NavItem("Register", 'register')
bookings_nav_item = NavItem("My Bookings", 'user_bookings')
account_nav_item = NavItem("Accounts", 'account_management')
film_mgt_nav_item = NavItem("Films", 'film_management')
booking_mgt_nav_item = NavItem("Bookings", 'booking_management')
club_mgt_nav_item = NavItem("Clubs", 'club_management')
user_mgt_nav_item = NavItem("Users", 'user_management')
screen_mgt_nav_item = NavItem("Screen", 'screens')
showing_mgt_nav_item = NavItem("Showing", 'showing')

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

# Get the user's group
def getGroup(user):
    # If the user doesn't belong to a group
    if len(user.groups.all()) == 0:
        # Return none
        return "None"
    # Otherwise return the user's group
    return user.groups.all()[0].name

# Render the page with the user's navigation items
def groupSpecificRender(request, page, context = {}):
    # Get the navigation items for the user
    context["nav_items"] = group_nav_dictionary[getGroup(request.user)]
    # Return the render of the 
    return render(request, page, context)