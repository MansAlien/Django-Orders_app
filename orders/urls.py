from django.urls import path
from .views import HomeListView, SettingsTemplateView, createview, categoryview, deleteview, renameview, applyview, cancelview

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("settings/", SettingsTemplateView.as_view(), name="settings"),
    path("settings/category/", categoryview, name="category_list"),
]


htmx_urlpatterns = [
    path("settings/category/create", createview, name="create"),
    path("settings/category/<int:pk>/rename/", renameview, name="rename"),
    path("settings/category/<int:pk>/apply/", applyview, name="apply"),
    path("settings/category/cancel/", cancelview, name="cancel"),
    path("settings/category/<int:pk>/delete", deleteview, name="delete"),
]

urlpatterns += htmx_urlpatterns
