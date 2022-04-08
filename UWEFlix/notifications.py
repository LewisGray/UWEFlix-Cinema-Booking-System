from django.dispatch import receiver
from UWEFlix.models import Notification
from datetime import datetime
from django.contrib.auth.models import User

# Function to send a notification to a user
def sendNotificationToUser(sender, receiver, message, href = None, href_data = None):
    # If the notification isn't being sent to themselves
    if sender != receiver:
        # Create a notification object
        notification = Notification.objects.create(receiver = receiver, message = message, seen = False, sent_date = datetime.now(), href = href, href_data = href_data)
        # Save the notification
        notification.save()

# Function to send a notification to a group of user
def sendNotificationToGroup(sender, group_name, message, href = None, href_data = None):
    # Get all the users of the specified group
    users = User.objects.filter(groups__name = group_name)
    # For each user
    for user in users:
        # If the notification isn't being sent to themselves
        if user != sender:
            # Create a notification object
            notification = Notification.objects.create(receiver = user, message = message, seen = False, sent_date = datetime.now(), href = href, href_data = href_data)
            # Save the notification
            notification.save()

# Get the notifications for a user
def getNotifications(user):
    # Return the notifications for the user
    return Notification.objects.filter(receiver = user)

# Get the number of notifications a user has
def countNewNotifications(user):
    # Get all the notifications
    notifications = Notification.objects.filter(receiver = user)
    # Get the notifications that haven't been seen
    notifications = notifications.filter(seen = False)
    # Return the number of notifications
    return len(notifications)

# Remove a notification linking to a specific request
def deleteNotification(href, href_data):
    # Get a notification with matching link and data
    notifications = Notification.objects.filter(href=href, href_data=href_data)
    # For each notification
    for notification in notifications:
        # Delete the notification
        notification.delete()