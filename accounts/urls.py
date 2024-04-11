from django.urls import path
from .views import SignUpView, EmployeeView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('employee_list/', EmployeeView.as_view(), name="employee_list"),
    path('signup/', SignUpView.as_view(), name='signup'),

    # Password reset links (refers to django.contrib.auth.views)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
