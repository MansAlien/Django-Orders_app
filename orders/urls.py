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

    path("cashier/", views.cashier_view, name="cashier"),
    path("settings/cashier/", views.cashier_settings_view, name="cashier_settings_view"),
    path("settings/cashier/customer", views.customer_view, name="customer_settings_view"),
    path("settings/cashier/order", views.order_view, name="order_view"),
    path("settings/cashier/order/order_details/<int:pk>", views.order_details_list, name="order_details"),
    

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
    path("cashier/customer_info/", views.customer_info, name="customer_info"),
    path("cashier/customer_with_id/", views.customer_with_id, name="customer_with_id"),

    # Customer
    path("cashier/clear_customer_info/", views.clear_customer_info, name="clear_customer_info"),
    path("cashier/create_customer/", views.create_customer, name="create_customer"),
    path("cashier/edit_customer/<int:pk>", views.edit_customer, name="edit_customer"),
    path("cashier/delete_customer/<int:pk>", views.delete_customer, name="delete_customer"),

    path("cashier/order_info/", views.new_order, name="order_info"),

    path("product_list/<int:pk>", views.product_list, name="product_list"),
    path("order_detail_row/<int:pk>", views.order_detail_row, name="order_detail_row"),
    path("order_payment/", views.order_payment, name="order_payment"),
    path("order_details_view/", views.order_details_view, name="order_details_view"),
    
    path("comment/create/<int:pk>", views.create_comment, name="create_comment"),
    path("comment/edit/<int:pk>", views.edit_comment, name="edit_comment"),
    path("comment/delete/<int:pk>", views.delete_comment, name="delete_comment"),

    path("editor", views.editor_view, name="editor_view"),
    path("editor/order_details/<int:pk>", views.editor_order_details, name="editor_order_details"),
    path("editor/order_details/comments/<int:pk>", views.editor_comments, name="editor_comments"),

    path('orders/files/<int:order_id>/', views.serve_order_file, name='serve_order_file'),
    path('orders/files/', views.open_folder, name='open_folder'),
]

urlpatterns += htmx_urlpatterns
