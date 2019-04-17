from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.my_login, name='login'),
    path('logout/', views.my_logout, name='logout'),
    path('forgot/', views.change_password, name='change_password'),
    path('index/', views.index, name='index'),
    path('detail/<int:poll_id>/', views.detail, name='poll_detail'),
    path('create/', views.create, name='create_poll'),
    path('detail/<int:poll_id>/create-comments/', views.create_comments, name='create_comments'),
    path('new-user/', views.newuser, name='newuser')
]
