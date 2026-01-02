from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # About page
    path('about/', views.about, name='about'),
    
    # Post-related URLs
    path('posts/', views.PostListView.as_view(), name='post_list'),
    path('posts/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('category/<int:category_id>/', views.category_posts, name='category_posts'),
    path('create/', views.create_post, name='create_post'),
    path('my-posts/', views.my_posts, name='my_posts'),
    
    # Comment URLs
    path('posts/<int:pk>/comment/', views.add_comment, name='add_comment'),
    
    # Like URLs (if you added them)
    path('posts/<int:pk>/like/', views.like_post, name='like_post'),
    
    # Search
    path('search/', views.search_posts, name='search'),
    
    # Profile URLs
    path('profile/', views.profile, name='profile'),
    
    # Authentication URLs
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),
]