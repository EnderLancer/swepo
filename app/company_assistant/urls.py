from django.urls import path
from django.contrib.auth import views as auth_views

from company_assistant import views

urlpatterns = [
    path("register", views.register_request, name="register"),
    path(
        "login", 
        auth_views.LoginView.as_view(
            template_name='company_assistant/login.html',
            next_page="home",
        ), 
        name='login'
    ),
    path("logout", auth_views.LogoutView.as_view(next_page="home"), name="logout"),

    path('', views.company_list, name='company_list'),
    path('create', views.company_create, name='company_create'),
    path("<int:company_id>", views.company_view, name="company"),
    path("<int:company_id>/specifics", views.company_specifics_change, name="company_specifics_change"),
]