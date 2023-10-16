from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import User, Todo


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2"]


class TodoForm(ModelForm):
    class Meta:
        model = Todo
        fields = ["name", "completed"]


class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ["avatar", "name", "email", "bio"]


class PasswordUpdateForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = "__all__"
