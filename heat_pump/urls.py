from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from heat_pump import views

urlpatterns = [
    path('heatPumps/', views.ConnectionList.as_view()),
    path('heatPumps/<str:device_id>/', views.ConnectionDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)