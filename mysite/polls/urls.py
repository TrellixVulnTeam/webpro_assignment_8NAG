from django.urls import path

from mysite.polls import views

urlpatterns = [
    path('index/', views.index, name='index')
]