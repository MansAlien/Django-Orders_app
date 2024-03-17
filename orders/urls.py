from django.urls import path
from .views import CatigoryListView, view_categories 

urlpatterns = [
    path("", CatigoryListView.as_view(), name="home"),
]


htmx_urlpatterns = [
    path("view_categories/", view_categories, name="view_categories"),
]

urlpatterns += htmx_urlpatterns
