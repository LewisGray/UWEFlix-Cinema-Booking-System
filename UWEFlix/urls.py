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
    path("film_management/", views.film_management_view, name="film_management"),
    path("account_management/", views.account_management_view, name="account_management"),
    path("representative/", views.representative_view, name="represent"),
    path("about/", views.about, name="about"), 
    path("login/", views.loginView, name="login"),
    path("logout/", views.userLogout, name="logout"),
    path("register/", views.register, name="register"),
    path("accesss_denied/", views.noAccess, name="no_access"),
    path("add_film/", views.log_film, name="add_film"),
    path("update_film/<str:filmName>", views.updateFilm, name="update_film"),
    path("remove_film/<str:filmName>", views.removeFilm, name="remove_film"), 
    # path("movies/", views.movies, name="movies"), 
]