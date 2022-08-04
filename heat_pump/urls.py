from django.urls import path
from heat_pump import views

urlpatterns = [
    path('heatPumps/', views.connection_list),
    path('heatPumps/<int:pk>/', views.connection_detail),
]
