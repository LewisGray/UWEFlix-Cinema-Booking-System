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