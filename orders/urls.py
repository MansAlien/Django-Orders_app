from django.urls import path
from .views import CategoryListView, SettingsTemplateView, createview, categoryview

urlpatterns = [
    path("", CategoryListView.as_view(), name="home"),
    path("settings/category/", categoryview, name="category_list"),
    path("settings/category/create", createview, name="create"),
]


htmx_urlpatterns = [
]

urlpatterns += htmx_urlpatterns
