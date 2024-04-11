from django.urls import path
from .views import home, login_time 

urlpatterns = [

    path('', home),
    path("login_time/<int:pk>/", login_time, name="login_time"),
]
