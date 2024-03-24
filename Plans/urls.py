from django.urls import path
from Plans.views import *

urlpatterns = [
    path('allplans', AllPlans.as_view(), name='allplans'),
]

app_name = 'Plans'