from django.urls import path

from . import views

app_name = 'vehicles'
urlpatterns = [
    path('', views.index, name='index'),
    path('<int:type_id>/', views.set_vehicle_type, name='settype'),
    path('vehicles/<int:pos>/', views.upd_vehicle_pos, name='updvehiclepos'),
    path('vehicles/del/<int:pos>/', views.del_vehicle_pos, name='delvehiclepos'),

]