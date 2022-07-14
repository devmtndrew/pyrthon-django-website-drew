from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages

from .models import Food, Customer
from .forms import FoodForm

# Create your views here.
def index(request):
    return HttpResponse('<p>Welcome to the GrubFood Kiosk!</p>')

def testview(request):
    return HttpResponse('<p>This is the test view!</p>')
    
def index(request):
    return render(request, 'webkiosk/welcome.html')

def listfood(request):
    fl = Food.objects.all()
    context = {
        'foodlist': fl
    }
    return render(request, 'webkiosk/food_list.html', context)

def createfood(request):
    if request.method =='GET':
        ff = FoodForm()
    elif request.method =='POST':
        ff = FoodForm(request.POST)
        if ff.is_valid():
            ff.save()
            return redirect('webkiosk:food-list')

    context = { 'form': ff }
    return render(request, 'webkiosk/food_form.html', context)

# bro i dont fucking know
def detailfood(request, pk):
    f = Food.objects.get(id=pk)
    context = { 'food':f }
    return render(request, 'webkiosk/food_detail.html', context)

def updatefood(request, pk):
    f = Food.objects.get(id=pk)
    if request.method == 'GET':
        ff = FoodForm(instance=f)
    elif request.method == 'POST':
        ff = FoodForm(request.POST, instance=f)
        if ff.is_valid():
            ff.save()
            messages.success(request, 'Food record updated')

    context = { 'form': ff }
    return render(request, 'webkiosk/food_form.html', context)

def deletefood(request, pk):
    f = Food.objects.get(id=pk)
    if request.method == 'GET':
        context = { 'food':f }
        return render(request, 'webkiosk/food_delete.html', context)
    elif request.method == 'POST':
        f.delete()
        return redirect('webkiosk:food-list')

def listcustomers(request):
    cl = Customer.objects.all()
    context = {
        'customerlist': cl
    }
    return render(request, 'webkiosk/customers_list.html', context)

