from django.urls import path
from .views import login_time 

urlpatterns = [
    path("login_time/<int:pk>/", login_time, name="login_time"),
]
