from django.forms import ModelForm
from .models import Food, Customer, Order
from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm

class FoodForm(ModelForm):
    class Meta:
        model = Food
        fields = ['name', 'description', 'price']

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['user','firstname','lastname','address','city']

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer','paymentmode','food', 'quantity']
