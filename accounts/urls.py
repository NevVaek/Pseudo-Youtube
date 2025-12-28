from django.urls import path
from .views import SignUpView, CustomUserCreationForm
from .forms import (CustomLoginForm, CustomPasswordChangeForm, CustomPasswordResetForm, CustomSetPasswordForm)
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    #path('login/', LoginView.as_view(), name='login'),  PROTOTYPE NOT USED
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomLoginForm), name='login'),
    path('password_change/', auth_views.PasswordChangeView.as_view(form_class=CustomPasswordChangeForm), name='password_change'),
    path('password_reset/', auth_views.PasswordResetView.as_view(form_class=CustomPasswordResetForm), name='password_reset'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=CustomSetPasswordForm), name="password_reset_confirm"),
]