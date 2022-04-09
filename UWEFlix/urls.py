from django.urls import path
from UWEFlix import views
from UWEFlix.models import Film
from django.contrib.auth import views as auth_views

# Establish the URLs
urlpatterns = [
    path("", views.student_view, name="home"),
    path("film_management/", views.film_management_view, name="film_management"),
    path("club_management/", views.club_management_view, name="club_management"),
    path("account_management/", views.account_management_view, name="account_management"),
    path("representative/", views.representative_view, name="represent"),
    path("about/", views.about, name="about"), 
    path("login/", views.loginView, name="login"),
    path("logout/", views.userLogout, name="logout"),
    path("register/", views.register, name="register"),
    path("account/", views.accountView, name="account"),
    path("accesss_denied/", views.noAccess, name="no_access"),
    
     path("reset_password/", 
        auth_views.PasswordResetView.as_view(template_name="UWEFlix/password_reset.html"), 
        name="reset_password"),

    path("reset_password_sent/", 
        auth_views.PasswordResetDoneView.as_view(template_name="UWEFlix/password_reset_sent.html"), 
        name="password_reset_done"),

    path("reset/<uidb64>/<token>/", 
        auth_views.PasswordResetConfirmView.as_view(template_name="UWEFlix/password_reset_form.html"), 
        name="password_reset_confirm"), # uidb64: users id encoded in base 64

    path("reset_password_complete/", 
        auth_views.PasswordResetCompleteView.as_view(template_name="UWEFlix/password_reset_done.html"), 
        name="password_reset_complete"),


    path("add_film/", views.log_film, name="add_film"),
    path("update_film/<str:filmName>", views.updateFilm, name="update_film"),
    path("remove_film/<str:object>", views.removeFilm, name="remove_film"),
    
    #Added paths for club rep CRUD
    path("add_clubRepresentative/", views.log_clubRepresentative, name="add_clubRepresentative"),
    path("update_clubRepresentative/<str:clubName>", views.updateClubRepresentative, name="update_clubRepresentative"),
    path("remove_clubRepresentative/<str:object>", views.removeClubRepresentative, name="remove_clubRepresentative"),
    path("clubRepresentative_management/", views.clubRepresentative_management_view, name="clubRepresentative_management"),
    ##############################

    path("add_club/", views.log_club, name="add_club"),
    path("update_club/<str:clubName>", views.updateClub, name="update_club"),
    path("remove_club/<str:object>", views.removeClub, name="remove_club"),
    
    path("add_booking/", views.log_booking, name="add_booking"),
    path("update_booking/<str:booking_id>", views.updateBooking, name="update_booking"),
    path("remove_booking/<str:booking_id>", views.removeBooking, name="remove_booking"),
    
    path("booking_management/", views.booking_management_view, name="booking_management"),
    path("add_user/", views.log_user, name="add_user"),
    path("update_user/<str:username>", views.updateUser, name="update_user"),
    path("remove_user/<str:username>", views.removeUser, name="remove_user"),
    
    path("user_management/", views.user_management_view, name="user_management"),
    path("my_bookings/", views.user_bookings, name="user_bookings"),
    path("add_account/", views.log_account, name="add_account"),
    path("update_account/<str:account_id>", views.updateAccount, name="update_account"),
    path("remove_account/<str:account_id>", views.removeAccount, name="remove_account"),
    path("account_management/", views.account_management_view, name="account_management"),
    # path("movies/", views.movies, name="movies"), 
    
        
    #Screens
    path("screen/", views.screen_view, name="screens"), 
    path("log_screens/", views.log_screens, name="log_screens"), 
    path("updateScreens/<str:object>", views.updateScreens, name="updateScreens"), 
    path("removeScreens/<str:object>", views.removeScreens, name="removeScreens"), 
    
    #Showing
    path("showing/", views.showing_view, name="showing"),
    path("addShowing/", views.log_showing, name="log_showing"), 
    path("updateShowing/<str:object>", views.updateShowings, name="updateShowings"), 
    path("removeShowings/<str:object>", views.removeShowings, name="removeShowings"), 
    
    # Booking urls
    path("book_film/<str:title>", views.bookFilm, name="book_film"),
    path("book_ticket/<str:showing_id>", views.bookTickets, name="book_ticket"),

    #Checkout url
    path("bookingComplete/", views.booking_complete, name="complete"),
    path("booking_success/", views.booking_success, name="success"),

    # Notifications
    path("notifications/", views.viewNotifications, name="notifications")
]