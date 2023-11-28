"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    # Endpoint for the main SPA
    path('', views.main_spa, name='main_spa'),

    # Endpoints to register, login and logout
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Endpoints for articles
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/category/<int:category_id>/', views.articles_by_category, name='articles_by_category'),
    path('articles/filtered/', views.filtered_articles, name='filtered_articles'),

    # Endpoint for categories
    path('categories/', views.category_list, name='category_list'),

    # Endpoints for user profile
    path('user/profile/', views.user_profile, name='user_profile'),

    # Endpoint for posting,replying,editing and deleting comments
    path('articles/<int:article_id>/comment/', views.post_comment, name='post_comment'),
    path('articles/<int:article_id>/comment/<int:parent_comment_id>/', views.post_comment, name='reply_comment'),
    path('edit-comment/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete-comment/<int:comment_id>/', views.delete_comment, name='delete_comment'),
]