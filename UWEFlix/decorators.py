from django.http import HttpResponse
from django.shortcuts import redirect

# Decorator to ensure user isn't logged in
def unauthenticated_required(view_function):
    # Establish the wrapper function
    def wrapper_function(request, *args, **kwargs):
        # If the user is authenticated
        if request.user.is_authenticated:
            # Redirect them to the hope page
            return redirect('/')
        # Otherwise
        else:
            # Return the provided function
            return view_function(request, *args, **kwargs)
    # Return the wrapper function
    return wrapper_function

# Decorator to ensure user is in the correct group
def permitted(roles=[]):
    # Establish the decorator function
    def decorator(view_function):
        # Establish the wrapper function
        def wrapper_function(request, *args, **kwargs):
            # Establish the user group as none
            user_group = None
            # If the user has a group
            if request.user.groups.exists():
                # Get the first user group from the user
                user_group = request.user.groups.all()[0].name
            # If the group is in the list of allowed roles
            if user_group in roles:
                # Return the provided function
                return view_function(request, *args, **kwargs)
            # Otherwise
            else:
                # Send the user to the no access page
                return redirect("no_access")
        # Return the wrapper function
        return wrapper_function
    # Return the decorator
    return decorator