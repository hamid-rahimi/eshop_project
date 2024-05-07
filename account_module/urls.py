from django.urls import path
from . import views


app_name = "account_module"
urlpatterns = [
    path('user-panel-dashboard/', views.UserPanelDashboardView.as_view(), name="user_panel_dashboard_page"),
    path('edit-user-profile/', views.EditUserProfileView.as_view(), name="edit_user_profile_page"),
    path('register/', views.RegisterView.as_view(), name="register_page"),
    path('active-account/<str:active_code>/', views.ActiveAccountView.as_view(), name="active_account_page"),
    path('login/', views.LoginView.as_view(), name="login_page"),
    path('logout/', views.LogoutView.as_view(), name="logout_page"),
    path('forget-pass/', views.ForgetPasswordView.as_view(), name="forget_pass_page"),
    path('change-pass/', views.ChangePasswordView.as_view(), name="change_pass_page"),
    path('reset-pass/<str:pass_ok>/', views.ResetPasswordView.as_view(), name="reset_pass_page"),
]
