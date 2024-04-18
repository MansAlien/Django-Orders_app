from django.urls import path
from .views import SignUpView, EmployeeView, employee_view, employee_detail_view, modal_view, step2_view, create_user, table_refresh, user_profile, cards,  user_update_view, user_update_profile, info_refresh
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('employee_list/', employee_view, name="employee_list"),
    path('signup/', SignUpView.as_view(), name='signup'),



    # Password reset links (refers to django.contrib.auth.views)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]

htmx_urlpatterns = [
    path('employee_list/', employee_view, name="employee_list"),
    path('employee_list/<int:pk>', employee_detail_view, name="employee_detail"),
    path('modal/', modal_view, name='modal'),
    path('step2/', step2_view, name='step2'),


    path('table_refresh/', table_refresh, name='table_refresh'),
    path('cards/', cards, name='cards'),
    path('create_user/', create_user, name='create_user'),
    path('employee_list/<int:pk>/edit_user/', user_update_view, name='edit_user'),
    path('employee_list/<int:pk>/edit_user_profile/', user_update_profile, name='edit_user_profile'),
    path('user_profile/<int:pk>', user_profile, name='user_profile'),


    path('info/<int:pk>/', info_refresh, name='info_refresh'),

]

urlpatterns += htmx_urlpatterns
