from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from .models import Customer, Food, Order
from .forms import FoodForm, CreateUserForm, CustomerForm
from .decorators import unauthenticated_user, allowed_users

# Create your views here.
def index(request):
    return redirect('../webkiosk/')

def index(request):
	return render(request, 'webkiosk/welcome.html')

def testview(request):
	return HttpResponse('<p>This is the test view!</p>')

#login_required restricts pages without login

@login_required(login_url='webkiosk:login')
@allowed_users(allowed_roles=['admin'])
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

def registerPage(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get('username')

			group = Group.objects.get(name='customer')
			user.groups.add(group)
			Customer.objects.create(
				user=user,
				firstname=user.username,
				)

			messages.success(request, 'Account was created for ' + username)

			return redirect('webkiosk:login')

	context = {'form':form}
	return render(request, 'webkiosk/register.html', context)

def loginPage(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('webkiosk:user-page')
		else:
			messages.info(request, 'Username OR Password is incorrect')


	context = {}
	return render(request, 'webkiosk/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('webkiosk:login')

@login_required(login_url='login')
def userPage(request):
	orders = request.user.customer.order_set.all()
	cl = Customer.objects.all()
	total_orders = orders.count()
	
	print('ORDERS:', orders)

	context = {'orders':orders, 'total_orders':total_orders,'customerlist':cl,}
	return render(request, 'webkiosk/user.html', context)

def updatecustomer2(request, pk):
	c = Customer.objects.get(id=pk) # declaring the variable c here to fill up the details
	if request.method == "GET":
		cf = CustomerForm(instance=c) # putting the details into the form
	elif request.method == "POST":
		cf = CustomerForm(request.POST, instance = c) # updates instance
		if cf.is_valid():
			cf.save()
			messages.success(request, "Customer record successfully updated.")

	context = {"customerform": cf} #context is the cf bc that's what we wanna pass to the html
	return render(request, 'webkiosk/customer_form_2.html', context)

def adminlogin(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('webkiosk:admin-home')
		else:
			messages.info(request, 'Username OR Password is incorrect')

	context = {}
	return render(request, 'webkiosk/admin_login.html', context)

@allowed_users(allowed_roles=['admin'])
def adminhome(request):
	fl = Food.objects.all()
	cl = Customer.objects.all()
	ol = Order.objects.all()

	context = {
		'foodlist': fl,
		'customerlist':cl,
		'orderlist': ol
	}

	return render(request, 'webkiosk/admin_home.html', context)

@allowed_users(allowed_roles=['admin'])
def createcustomer(request):
	if request.method == "GET":
		cf = CustomerForm()
	elif request.method == "POST":
		cf = CustomerForm(request.POST)
		if cf.is_valid():
			cf.save()
		return redirect('webkiosk:customers-list')
	
	context = {"customerform" :  cf}
	return render(request, "webkiosk/customer_form.html", context)

@allowed_users(allowed_roles=['admin'])
def detailcustomer(request,pk):
	c = Customer.objects.get(id=pk)
	context = {'customer': c}
	return render(request, "webkiosk/customer_detail.html", context)

@allowed_users(allowed_roles=['admin'])
def updatecustomer(request, pk):
	c = Customer.objects.get(id=pk) # declaring the variable c here to fill up the details
	if request.method == "GET":
		cf = CustomerForm(instance=c) # putting the details into the form
	elif request.method == "POST":
		cf = CustomerForm(request.POST, instance = c) # updates instance
		if cf.is_valid():
			cf.save()
			messages.success(request, "Customer record successfully updated.")

	context = {"customerform": cf} #context is the cf bc that's what we wanna pass to the html
	return render(request, 'webkiosk/customer_form.html', context)

@allowed_users(allowed_roles=['admin'])
def deletecustomer(request, pk):
	c = Customer.objects.get(id=pk)
	if request.method == "GET":
		context = {"customer":c}
		return render(request, 'webkiosk/customer_delete.html', context)
	elif request.method == "POST":
		c.delete()
		return redirect('webkiosk:customers-list')