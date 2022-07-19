from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import Group, User, Permission 
from django.contrib.contenttypes.models import ContentType

from .models import Customer, Food, Order
from .forms import FoodForm, CreateUserForm, CustomerForm, OrderForm
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

@login_required(login_url='login')
def updatecustomer2(request, pk):
	current_user = request.user
	c = Customer.objects.get(user=pk) # declaring the variable c here to fill up the details
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
    o = Order.objects.filter(customer_id=pk)
    context = {'customer': c, 'order': o}
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

@login_required(login_url='webkiosk:login')
def listfood2(request):
	fl = Food.objects.all()
	context = {
		'foodlist': fl
	}
	return render(request, 'webkiosk/food_list2.html', context)

#add order for admin
@login_required(login_url='webkiosk:login')
def addorder(request):
	if request.method == "GET":
		of = OrderForm()
	elif request.method == 'POST':
		of = OrderForm(request.POST)
		if of.is_valid():
			of.save()
		return redirect('webkiosk:admin-home')

	context = {'orderform' : of}
	return render(request, "webkiosk/order_form.html", context)

#update order
@login_required(login_url='login')
def updateorder(request, pk):
 # declaring the variable c here to fill up the details
    o = Order.objects.get(id=pk)
    if request.method == "GET":
        of = OrderForm(instance=o) # putting the details into the form
    elif request.method == "POST":
        of = OrderForm(request.POST, instance = o) # updates instance
        if of.is_valid():
            of.save()
        
    context = {"orderform": of} #context is the cf bc that's what we wanna pass to the html
    return render(request, 'webkiosk/order_form.html', context)

#delete order
@login_required(login_url='login')
def deleteorder(request,pk):
    
    o = Order.objects.get(id=pk)
    if request.method == 'GET':
        context = {'order': o} 
        return render(request, 'webkiosk/order_delete.html', context)
    elif request.method == "POST":
        o.delete()
        return redirect('webkiosk:admin-home')

#add order for admin
@login_required(login_url='webkiosk:login')
def addorder2(request):
	if request.method == "GET":
		of = OrderForm()
	elif request.method == 'POST':
		of = OrderForm(request.POST)
		if of.is_valid():
			of.save()
		return redirect('webkiosk:admin-home')

	context = {'orderform' : of}
	return render(request, "webkiosk/order_form2.html", context)

#update order
@login_required(login_url='login')
def updateorder2(request, pk):
 # declaring the variable c here to fill up the details
    o = Order.objects.get(id=pk)
    if request.method == "GET":
        of = OrderForm(instance=o) # putting the details into the form
    elif request.method == "POST":
        of = OrderForm(request.POST, instance = o) # updates instance
        if of.is_valid():
            of.save()
        
    context = {"orderform": of} #context is the cf bc that's what we wanna pass to the html
    return render(request, 'webkiosk/order_form2.html', context)

#delete order
@login_required(login_url='login')
def deleteorder2(request,pk):
    
    o = Order.objects.get(id=pk)
    if request.method == 'GET':
        context = {'order': o} 
        return render(request, 'webkiosk/order_delete2.html', context)
    elif request.method == "POST":
        o.delete()
        return redirect('webkiosk:admin-home')

#add order for admin
@login_required(login_url='webkiosk:login')
def addorder2(request):
	if request.method == "GET":
		of = OrderForm()
	elif request.method == 'POST':
		of = OrderForm(request.POST)
		if of.is_valid():
			of.save()
		return redirect('webkiosk:admin-home')

	context = {'orderform' : of}
	return render(request, "webkiosk/order_form2.html", context)
