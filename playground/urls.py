from django.urls import path
from .views import *


urlpatterns = [
    # path('start',hello,name='hello'),
    path('start/',HelloView.as_view())
]