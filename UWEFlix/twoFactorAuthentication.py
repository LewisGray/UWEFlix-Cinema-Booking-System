from UWEFlix.render import dynamicRender
from django.shortcuts import redirect
from django.contrib.auth import views as auth_views 

# Return the 2FA settings page
def twoFactorSettings(request):
    # Return the user to their homepage
    return dynamicRender(request, "UWEFlix/student.html")