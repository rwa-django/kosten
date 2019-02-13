from django.urls import path

from . import views

app_name = 'vehicles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:type_id>/', views.set_vehicle_type, name='settype'),

]