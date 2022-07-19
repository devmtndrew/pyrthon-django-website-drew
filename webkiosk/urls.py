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
    path("user/<str:pk>/edit/", views.updatecustomer2, name='customer-update-2'),
    path('foodmenu/', views.listfood2, name='food-list-2'),
    path('admin/order/add/', views.addorder, name="add-order"),
    path('user/order/add/', views.addorder2, name="add-order-2"),
    path('admin/order/<int:pk>/edit/', views.updateorder, name="edit-order"),
    path('admin/order/<int:pk>/delete/',views.deleteorder, name="delete-order"),
    path('user/order/add/', views.addorder2, name="add-order-2"),
    path('user/order/<int:pk>/edit/', views.updateorder2, name="edit-order-2"),
    path('user/order/<int:pk>/delete/',views.deleteorder2, name="delete-order-2"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)