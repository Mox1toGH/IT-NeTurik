from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('singup/', views.singup_view, name='singup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
