from UWEFlix.models import Showing, Booking, User
#
class ListWidget():
    # On creation
    def __init__(self, title, items):
        #
        self.title = title
        #
        self.items = items
        #
        self.type = "list"

#
class ButtonWidget():
    # On creation
    def __init__(self, title, buttons, hrefs):
        #
        self.title = title
        #
        self.buttons = []
        #
        for i, text in enumerate(buttons):
            #
            self.buttons.append(Button(text, hrefs[i]))
        #
        self.type = "button"

#
class Button():
    # On creation
    def __init__(self, text, href):
        #
        self.text = text
        #
        self.href = href

#
def getWidgets(group):
    #
    widgets = []
    #
    if group == "Cinema Manager" or group == "Cinema Employee" or group == "Admin":
        #
        showings = Showing.objects.order_by('date').order_by('time')[:10]
        #
        bookings = Booking.objects.order_by('time_booked')[:5]
        #
        widgets.append(ListWidget("Upcoming Showings", [f"{i.film.title} in Screen {i.screen.number} at {i.date}, {i.time}" for i in showings]))
        #
        widgets.append(ButtonWidget("Quick Actions", ["Add Film", "Add Showing", "Add Screen", "Add Club"], ["add_film", "log_showing", "log_screens", "add_club"]))
        #
        widgets.append(ListWidget("Recent Bookings", [f"{i.customer.username} booked showing {i.showing.id} at {i.time_booked}" for i in bookings]))
    #
    elif group == "Account Manager":
        #
        bookings = Booking.objects.order_by('time_booked')
        #
        customers = User.objects.all()
        #
        customer_list = []
        #
        for customer in customers:
            #
            customer_list.append([customer, 0])
        #
        for booking in bookings:
            #
            for item in customer_list:
                #
                if item[0] == booking.customer:
                    #
                    item[1] = item[1] + booking.cost
            #
        sorted_list = sorted(customer_list, key=lambda x: x[1], reverse=True)
        #
        widgets.append(ListWidget("Recent Bookings", [f"{i.customer.username} booked showing {i.showing.id} at {i.time_booked}" for i in bookings[:5]]))
        #
        widgets.append(ButtonWidget("Quick Actions", ["Add Account", "Add Club", "View Statements"], ["add_account", "add_club", "add_account"]))
        #
        widgets.append(ListWidget("Top Customers", [f"{i[0].username} has spent £{round(i[1], 2)}" for i in sorted_list[:10]]))

    #
    return widgets