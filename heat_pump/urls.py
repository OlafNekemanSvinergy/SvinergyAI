from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from heat_pump import views
from heat_pump.scheduled_events import setup_background_scheduler

urlpatterns = [
    path('heatPumps/', views.ConnectionList.as_view()),
    path('heatPumps/<str:device_id>/', views.ConnectionDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)

back_sched = setup_background_scheduler()
back_sched.start()
