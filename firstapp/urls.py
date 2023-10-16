from django.urls.conf import path
from firstapp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("create", views.createTodo, name="create_todo"),
    path("about", views.aboutPage, name="about"),
    path("update/<str:pk>", views.updateTodo, name="todo_update"),
    path("delete/<str:pk>", views.deleteTodo, name="todo_delete"),

    path("register", views.registerUser, name="register"),
    path("login/", views.loginPage, name="login"),
    path("logout", views.logoutUser, name="logout"),
    path("user-update", views.updateUser, name="user_update"),
    path("user-delete/<str:pk>", views.deleteUser, name="user_delete"),
    path("password-update", views.updatePassword, name="password_update"),
]
