from django.db import models
from django.contrib.auth.models import AbstractUser

class Category(models.Model):
    name = models.CharField(max_length=100)

class User(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    favorite_categories = models.ManyToManyField(Category, blank=True)

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author_name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    parent_comment = models.ForeignKey('self', related_name='replies', on_delete=models.CASCADE, null=True, blank=True)

