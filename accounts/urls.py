from django.urls import path
from .views import SignUpView, EmployeeView, employee_view, employee_detail_view, info, log, permissions, modal_view, step2_view, create_user, table_refresh
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('employee_list/', employee_view, name="employee_list"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('create-user/', create_user, name='create_user'),
    path('table_refresh/', table_refresh, name='table_refresh'),



    # Password reset links (refers to django.contrib.auth.views)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

htmx_urlpatterns = [
    path('employee_list/', employee_view, name="employee_list"),
    path('employee_list/<int:pk>', employee_detail_view, name="employee_detail"),
    path('info', info, name='info'),
    path('log/', log, name='log'),
    path('permissions/', permissions, name='permissions'),
    path('modal/', modal_view, name='modal'),
    path('step2/', step2_view, name='step2'),

]

urlpatterns += htmx_urlpatterns
