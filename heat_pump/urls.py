from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from heat_pump import views

urlpatterns = [
    path('heatPumps/', views.connection_list),
    path('heatPumps/<int:pk>/', views.connection_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)