# from django.contrib.auth import views as auth_views
from django.urls import path

from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add/', views.add_attendance, name="add-attendance"),
    path('live/', views.get_attendance, name="get-attendance")

    # path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
]
