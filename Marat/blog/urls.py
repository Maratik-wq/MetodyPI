from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.HomeClubListView.as_view(), name='home'),          
    path('search/', views.SearchView.as_view(), name='search'),        
    path('posts/', views.PostListView.as_view(), name='post_list'),    
    path('club/<int:pk>/', views.ClubDetailView.as_view(), name='club_detail'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('register/', views.register, name='register'),
]