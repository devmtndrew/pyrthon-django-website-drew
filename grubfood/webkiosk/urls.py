from django.urls import path
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
    path('customer/', views.listcustomers, name='customers-list')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)