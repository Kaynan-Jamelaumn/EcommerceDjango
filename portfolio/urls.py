from django.urls import path, include
from django.shortcuts import render
from . import views
app_name = "portfolio"
urlpatterns = [
    path('', views.portfolio, name="portfolio")

]
