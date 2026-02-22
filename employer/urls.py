from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('emp_dash/', views.emp_dash, name='emp_dash'),
    path('emp_das/', views.emp_dash),
    path('add_job/', views.add_job, name='add_job'),
    path('emp_job/', views.emp_job, name='emp_job'),
]
