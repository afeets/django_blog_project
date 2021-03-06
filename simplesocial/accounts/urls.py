from django.urls import path,re_path,include
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    re_path(r'login/$',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),
    re_path(r'logout/$',auth_views.LogoutView.as_view(),name='logout'), # by default returns to homepage
    re_path(r'signup/$',views.Signup.as_view(),name='signup'),
]
