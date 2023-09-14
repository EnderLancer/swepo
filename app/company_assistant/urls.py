from django.contrib import admin
from django.urls import include, path

from company_assistant import views

urlpatterns = [
    path("home/", views.employer_page, name="employer_home"),
]