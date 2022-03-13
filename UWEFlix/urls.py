from django.urls import path
from UWEFlix import views
from UWEFlix.models import Film

# Get the main student view from the StudentFilmListView class
student_film_list_view = views.StudentFilmListView.as_view(
    # Use the student.html page
    template_name = "UWEFlix/student.html"
)

# Establish the URLs
urlpatterns = [
    # path("", views.student_view, name="home"),
    path("", student_film_list_view, name="home"), #home screen will be placeholder
    path("cinema_management/", views.cinema_management_view, name="cinema_management"),
    path("account_management/", views.account_management_view, name="account_management"),
    path("representative/", views.representative_view, name="represent"),
    path("about/", views.about, name="about"), 
    path("login/", views.login, name="login"), 
    path("temp_film_creator/", views.temp_log_film, name="temp_film_creator"), # A temporary page to add films to the database
    # path("movies/", views.movies, name="movies"), 
]