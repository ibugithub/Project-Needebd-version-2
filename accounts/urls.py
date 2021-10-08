from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import *
urlpatterns  = [
    # -->The Mistake I've done previously---->  path('', views.myRegisterView().as_view(), name ='tregister')
    path('register/', views.RegistrationView.as_view(), name='tregister'),
    path('activate/<uidb64>/<token>',views.ActivateAccountView.as_view(), name='activate'),
    # path('verify/', views.verify_view, name = 'verify_view'),
    path('login/', views.log_in, name = 'login'),
    path('logout/', views.log_out , name = 'logout'),
    path('changepass/',auth_views.PasswordChangeView.as_view(template_name = 'accounts/changepassword.html', form_class = password_user_change, success_url = '/accounts/changepassdone/'), name= 'changepass'),
    path('changepassdone/', auth_views.PasswordChangeDoneView.as_view(template_name = 'accounts/password-change-done.html'), name = 'change_pass_done'),

    
    path('passwordreset/', auth_views.PasswordResetView.as_view(template_name ='accounts/password_reset.html', form_class = MyPasswordResetForm), name = 'password_reset'),

    path('password-reset-done/', auth_views.PasswordResetView.as_view(template_name ='accounts/password_reset_done.html'), name = 'password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/password_reset_confirm.html' ,form_class = MySetPasswordForm), name = 'password_reset_confirm'),

    path('password-reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_reset_complete.html'), name ='password_reset_complete'),

    path('resend-gmail-verification-link-url/', views.ResendGmailVerificationLink, name='resend-gmail-verification-link-url-name')

]