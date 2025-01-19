from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('home/', views.home, name="home"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create_room/', views.createRoom, name= "create-room"),
    path('update_room/<str:pk>/', views.updateRoom, name= "update_room"),
    path('delete_room/<str:pk>/', views.deleteRoom, name="delete_room"),
    path('login/', views.LoginPage, name="login"),
    path('register/', views.registerUser, name="register"),
    path('logout/',views.logoutUser, name= "logout"),
    path('delete-message/<str:pk>/', views.deleteMessage,name="delete-message"),
    path('profile/<str:pk>/', views.userProfile, name= 'user-profile'),
    path('update-user/', views.updateUser, name="update-user")
]
