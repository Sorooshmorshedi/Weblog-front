from django.urls import path, include

from . import views

app_name = 'accounts'
urlpatterns = [
    path('signup',views.SignUpView, name='signup'),
    path('login', views.LoginView, name='login'),
    path('logout', views.LogoutView, name='logout'),

]
