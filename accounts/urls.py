from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    EmployeeView,
    SignUpView,
    cards,
    create_deduction_view,
    create_user,
    deduction,
    employee_detail_view,
    info,
    log,
    permission_view,
    reset_password,
    table_refresh,
    user_profile,
    user_update_profile,
    user_update_view,
)

urlpatterns = [
    path("employee_list/", EmployeeView.as_view(), name="employee_list"),
    path("employee_list/<int:pk>", employee_detail_view, name="employee_detail"),
    # Password reset links (refers to django.contrib.auth.views)
    path("signup/", SignUpView.as_view(), name="signup"),
    path( "password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path( "password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done",),
    path( "reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm",),
    path( "reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete",),
    # for the admin
    path("reset_password/<int:user_id>/", reset_password, name="reset_password"),
]

htmx_urlpatterns = [
    path("create_user/", create_user, name="create_user"),
    path("employee_list/<int:pk>/edit_user/", user_update_view, name="edit_user"),
    path( "employee_list/<int:pk>/edit_user_profile/", user_update_profile, name="edit_user_profile",),
    path("user_profile/<int:pk>", user_profile, name="user_profile"),
    
    #tabs
    path("info/<int:pk>/", info, name="info"),
    path("log/<int:pk>/", log, name="log"),
    path("deduction/<int:pk>", create_deduction_view, name="create_deduction"),
    path("permissions/<int:pk>", permission_view, name="permissions"),
    path("deduction_refresh/<int:pk>/", deduction, name="deduction"),

    path("table_refresh/", table_refresh, name="table_refresh"),
    path("cards/", cards, name="cards"),
]

urlpatterns += htmx_urlpatterns
