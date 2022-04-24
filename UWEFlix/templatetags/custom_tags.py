from django import template

# Get register from the library
register = template.Library() 

# Create a filter to check if a user is in a group
@register.filter(name='has_group')
def has_group(user, group_name):
    # Return whether the group name exists in the user groups
    return user.groups.filter(name=group_name).exists() 

# Create a filter to check if the user is logged in
@register.filter(name='logged_in')
def logged_in(user):
    # Return whether the user is authenticated
    return user.is_authenticated

# Check if an item is a link
@register.filter(name='is_link')
def is_link(item):
    # If the type is a link
    if item.type == "link":
        # Return True
        return True
    # Else, return false
    return False

# Check if an item is a notification
@register.filter(name='is_notification')
def is_notification(item):
    # If the type is a notification
    if item.type == "notification":
        # Return True
        return True
    # Else, return false
    return False

# Check if an item is text
@register.filter(name='is_text')
def is_text(item):
    # If the type is text
    if item.type == "text":
        # Return True
        return True
    # Else, return false
    return False

# Check if unseen notifications
@register.filter(name='unseen_notifications')
def unseen_notifications(item):
    # If the count is more than 0
    if item.count > 0:
        # Return True
        return True
    # Else, return false
    return False

# Check if a widget is a list
@register.filter(name='is_list')
def is_list(widget):
    # If the widget is a list
    if widget.type == "list":
        # Return True
        return True
    # Else, return false
    return False

# Check if a widget is a button
@register.filter(name='is_button')
def is_button(widget):
    # If the widget is button
    if widget.type == "button":
        # Return True
        return True
    # Else, return false
    return False