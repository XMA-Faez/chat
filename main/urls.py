from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('find-user/', views.find_user_view, name='find_user'),
    path('chat/<int:room_id>/', views.chat_room_view, name='chat_room'),
]