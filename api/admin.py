from django.contrib import admin
from .models import Article, User, Category, Comment

admin.site.register(Article)
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Comment)
