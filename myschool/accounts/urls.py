from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.singup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('edit/', views.edit_account_view, name='edit_account'),
    path('delete/', views.delete_account_view, name='delete_account'),
]
