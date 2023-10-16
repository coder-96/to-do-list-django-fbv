from django.urls import path
from . import views

urlpatterns = [
    path("", views.getRoutes),
    path("todo/", views.getTodos),
    path("todo/<str:pk>", views.getTodo),
]