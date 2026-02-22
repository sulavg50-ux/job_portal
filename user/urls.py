from django.urls import path
from . import views

urlpatterns = [
    path('user_reg/', views.user_reg, name='user_reg'),
    path('user_log/', views.user_log, name='user_log'),
    path('user_dash/', views.user_dash, name='user_dash'),
   
]