from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Article, Comment, User, Category
from django.views.decorators.csrf import csrf_exempt
import json

def main_spa(request):
    return HttpResponse('Main SPA Page')

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        birth_date = request.POST.get('birth_date')
        profile_image = request.FILES.get('profile_image')

        try:
            user = User.objects.create_user(username=username, password=password)
            if birth_date:
                user.birth_date = birth_date
            if profile_image:
                user.profile_image = profile_image
            user.save()

            return JsonResponse({'status': 'success', 'message': 'User registered successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def logout_view(request):
    logout(request)
    return JsonResponse({'message': 'Logout successful'}, status=200)

def article_list(request):
    articles = list(Article.objects.values('id', 'title', 'category__name', 'author_name'))
    return JsonResponse({'articles': articles}, safe=False)

def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = list(Comment.objects.filter(article=article).values('id', 'content', 'author__username'))
    article_data = {
        'title': article.title,
        'content': article.content,
        'author': article.author_name,
        'comments': comments
    }
    return JsonResponse(article_data)

@login_required
def filtered_articles(request):
    user = request.user
    favorite_categories = user.favorite_categories.all()
    articles = Article.objects.filter(category__in=favorite_categories).values('id', 'title', 'category__name', 'author_name')
    return JsonResponse({'articles': list(articles)}, safe=False)

def category_list(request):
    categories = list(Category.objects.values('id', 'name'))
    return JsonResponse({'categories': categories}, safe=False)

def articles_by_category(request, category_id):
    articles = list(Article.objects.filter(category_id=category_id).values('id', 'title', 'author_name'))
    return JsonResponse({'articles': articles}, safe=False)

@csrf_exempt
@login_required
def user_profile(request):
    user = request.user

    if request.method == 'GET':
        favorite_categories_ids = user.favorite_categories.values_list('id', flat=True)
        user_data = {
            'username': user.username,
            'email': user.email,
            'birth_date': user.birth_date.isoformat() if user.birth_date else None,
            'profile_image': user.profile_image.url if user.profile_image else None,
            'favorite_categories': list(favorite_categories_ids),
        }
        return JsonResponse(user_data)

    elif request.method == 'POST':
        user.email = request.POST.get('email', user.email)
        user.birth_date = request.POST.get('birth_date', user.birth_date)
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user.profile_image.save(profile_image.name, profile_image)
        user.save()
        return JsonResponse({'message': 'Profile updated successfully'})
    else:
        return HttpResponse(status=405)

@csrf_exempt
@login_required
def post_comment(request, article_id, parent_comment_id=None):
    article = get_object_or_404(Article, id=article_id)
    data = json.loads(request.body)
    comment_content = data.get('comment')
    if parent_comment_id:
        parent_comment = get_object_or_404(Comment, id=parent_comment_id)
        Comment.objects.create(article=article, author=request.user, content=comment_content, parent_comment=parent_comment)
    else:
        Comment.objects.create(article=article, author=request.user, content=comment_content)
    return JsonResponse({'message': 'Comment added successfully'})

@csrf_exempt
@login_required
def edit_comment(request, comment_id):
    if request.method == 'PUT':
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        data = json.loads(request.body)
        comment_content = data.get('comment')
        comment.content = comment_content
        comment.save()
        return JsonResponse({'message': 'Comment updated successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
@login_required
def delete_comment(request, comment_id):
    if request.method == 'DELETE':
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        comment.delete()
        return JsonResponse({'message': 'Comment deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
