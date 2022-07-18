from django.urls import path, include
from . import views 
from django.conf import settings
from django.conf.urls.static import static

app_name = 'webkiosk'
urlpatterns = [
    path('', views.index, name='index'),
    path('testview/', views.testview, name='testview'),
    path('food/', views.listfood, name='food-list'),
    path('food/new/', views.createfood, name='food-create'),
    path('food/<int:pk>', views.detailfood , name='food-detail'),
    path('food/<int:pk>/edit', views.updatefood, name='food-update'),
    path('food/<int:pk>/delete/', views.deletefood, name='food-delete'),
    path('customer/', views.listcustomers, name='customers-list'),
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user/', views.userPage, name='user-page'),
    path('admin-login/', views.adminlogin, name='admin-login'),
    path('admin-home/', views.adminhome, name='admin-home'), 
    path('customers/new/', views.createcustomer, name='customer-create'),
    path("customers/<int:pk>", views.detailcustomer, name="customer-detail"),
    path("customers/<int:pk>/edit/", views.updatecustomer, name='customer-update'),
    path('customers/<int:pk>/delete/', views.deletecustomer, name="customer-delete"),
    path("user/<int:pk>/edit/", views.updatecustomer2, name='customer-update-2'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)