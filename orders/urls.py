from django.urls import path
from .views import CatigoryListView

urlpatterns = [
    path("", CatigoryListView.as_view(), name="home"),
]
