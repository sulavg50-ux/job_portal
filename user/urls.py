from django.urls import path
from . import views

urlpatterns = [
    path('user_reg/', views.user_reg, name='user_reg'),
    path('user_log/', views.user_log, name='user_log'),
    path('user_dash/', views.user_dash, name='user_dash'),
    path('application/',views.application,name='application'),
    path('view_app/', views.view_app, name='view_app'),
    path('delete_application/<int:application_id>/', views.delete_application, name='delete_application'),
]
