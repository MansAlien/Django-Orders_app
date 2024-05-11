from django.urls import path
from orders import views

urlpatterns = [
    path("", views.HomeListView.as_view(), name="home"),
    path("settings/", views.SettingsTemplateView.as_view(), name="settings"),

    path("settings/inventory/", views.inventory_view, name="inventory"),
    path("settings/inventory/category", views.category_view, name="category"),
    path("settings/inventory/attribute", views.attributes_view, name="attribute"),
    path("settings/inventory/product", views.product_view, name="product"),
    path("settings/inventory/product_line", views.product_line_view, name="product_line"),
]


htmx_urlpatterns = [
    # category
    path("settings/inventory/category/create", views.create_category, name="create_category"),
    path("settings/inventory/category/<int:pk>/edit", views.edit_category, name="edit_category"),

    # sub_category
    path("settings/inventory/sub_category/create", views.create_sub_category, name="create_sub_category"),
    path("settings/inventory/sub_category/<int:pk>/edit", views.edit_sub_category, name="edit_sub_category"),

    # Attribute
    path("settings/inventory/attribute/create", views.create_attribute, name="create_attribute"),
    path("settings/inventory/attribute/<int:pk>/edit", views.edit_attribute, name="edit_attribute"),
]

urlpatterns += htmx_urlpatterns
