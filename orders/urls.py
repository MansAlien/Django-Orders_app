from django.urls import path
from .views import HomeListView, SettingsTemplateView, categorycreateview, category_view, categorydeleteview, categoryrenameview, categoryapplyview, categorycancelview, subcategoryview, subcategorycreateview, subcategoryrenameview, subcategoryapplyview, subcategorycancelview, subcategorydeleteview, inventory_view
from orders import views

urlpatterns = [
    path("", HomeListView.as_view(), name="home"),
    path("settings/", SettingsTemplateView.as_view(), name="settings"),
    path("settings/subcategory/", subcategoryview, name="subcategory"),
    path("settings/inventory/", inventory_view, name="inventory"),
]


htmx_urlpatterns = [

    path("settings/inventory/category", category_view, name="category"),
    path("settings/inventory/category/create", views.create_category, name="create_category"),
    path("settings/inventory/category/<int:pk>/edit", views.edit_category, name="edit_category"),
    path("settings/inventory/sub_category/create", views.create_sub_category, name="create_sub_category"),
    path("settings/inventory/sub_category/<int:pk>/edit", views.edit_sub_category, name="edit_sub_category"),


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
