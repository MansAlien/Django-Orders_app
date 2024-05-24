from django.urls import path
from orders import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("settings/", views.SettingsTemplateView.as_view(), name="settings"),
    path("dashboard/inventory", views.inventory_dashboard_view, name="inventory_dashboard"),

    path("settings/inventory/", views.inventory_view, name="inventory"),
    path("settings/inventory/category", views.category_view, name="category"), # category & sub_category
    path("settings/inventory/attribute", views.attributes_view, name="attribute"), # attributes & products
    path("settings/inventory/product_line", views.product_line_view, name="product_line"), # attribute_value & product_line
]


htmx_urlpatterns = [
    # category
    path("settings/inventory/category/create", views.create_category, name="create_category"),
    path("settings/inventory/category/<int:pk>/edit", views.edit_category, name="edit_category"),
    path("settings/inventory/category/<int:pk>/delete", views.delete_category, name="delete_category"),

    # sub_category
    path("settings/inventory/sub_category/create", views.create_sub_category, name="create_sub_category"),
    path("settings/inventory/sub_category/<int:pk>/edit", views.edit_sub_category, name="edit_sub_category"),
    path("settings/inventory/sub_category/<int:pk>/delete", views.delete_sub_category, name="delete_sub_category"),

    # Attribute
    path("settings/inventory/attribute/create", views.create_attribute, name="create_attribute"),
    path("settings/inventory/attribute/<int:pk>/edit", views.edit_attribute, name="edit_attribute"),
    path("settings/inventory/attribute/<int:pk>/delete", views.delete_attribute, name="delete_attribute"),

    # Product
    path("settings/inventory/product/create", views.create_product, name="create_product"),
    path("settings/inventory/prodcut/<int:pk>/edit", views.edit_product, name="edit_product"),
    path("settings/inventory/product/<int:pk>/delete", views.delete_product, name="delete_product"),

    # Attribute Value
    path("settings/inventory/attribute_value/create", views.create_attribute_value, name="create_attribute_value"),
    path("settings/inventory/attribute_value/<int:pk>/edit", views.edit_attribute_value, name="edit_attribute_value"),
    path("settings/inventory/attribute_value/<int:pk>/delete", views.delete_attribute_value, name="delete_attribute_value"),

    # Product_line
    path("settings/inventory/product_line/create", views.create_product_line, name="create_product_line"),
    path("settings/load_product_values/", views.load_product_values, name="load_product_values"),
    path("settings/inventory/prodcut_line/<int:pk>/edit", views.edit_product_line, name="edit_product_line"),
    path("settings/inventory/product_line/<int:pk>/delete", views.delete_product_line, name="delete_product_line"),

    # Cashier
    path("cashier/", views.cashier_view, name="cashier"),
    path("product_list/<int:pk>", views.product_list, name="product_list"),
]

urlpatterns += htmx_urlpatterns
