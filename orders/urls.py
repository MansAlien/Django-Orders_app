from django.urls import path
from .views import HomeListView, SettingsTemplateView, categorycreateview, categoryview, categorydeleteview, categoryrenameview, categoryapplyview, categorycancelview, subcategoryview, subcategorycreateview, subcategoryrenameview, subcategoryapplyview, subcategorycancelview, subcategorydeleteview

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("settings/", SettingsTemplateView.as_view(), name="settings"),
    path("settings/category/", categoryview, name="category_list"),
    path("settings/subcategory/", subcategoryview, name="subcategory"),
]


htmx_urlpatterns = [
    path("settings/category/create", categorycreateview, name="create"),
    path("settings/category/<int:pk>/rename/", categoryrenameview, name="rename"),
    path("settings/category/<int:pk>/apply/", categoryapplyview, name="apply"),
    path("settings/category/cancel/", categorycancelview, name="cancel"),
    path("settings/category/<int:pk>/delete", categorydeleteview, name="delete"),
    
    
    path("settings/subcategory/create_sub", subcategorycreateview, name="create_sub"),
    path("settings/subcategory/<int:pk>/rename", subcategoryrenameview, name="rename_sub"),
    path("settings/subcategory/<int:pk>/apply/", subcategoryapplyview, name="apply_sub"),
    path("settings/subcategory/<int:pk>/cancel/", subcategorycancelview, name="cancel_sub"),
    path("settings/subcategory/<int:pk>/delete/", subcategorydeleteview, name="delete_sub"),
]

urlpatterns += htmx_urlpatterns
