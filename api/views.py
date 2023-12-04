from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Article, Comment, User, Category
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import default_storage
import json
from django.core.files.base import ContentFile
import base64
import datetime

def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # Parse JSON data for username, password, and birth date
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        birth_date = data.get('birth_date')

        # Create user
        try:
            user = User.objects.create_user(username=username, password=password)
            if birth_date:
                user.birth_date = datetime.datetime.strptime(birth_date, '%Y-%m-%d').date()
            user.save()

            # Handle profile image if present
            if 'profile_image' in data:
                format, imgstr = data['profile_image'].split(';base64,')
                ext = format.split('/')[-1]

                file = ContentFile(base64.b64decode(imgstr), name=f'{username}.{ext}')
                user.profile_image.save(name=f'{username}.{ext}', content=file, save=True)

            auth_login(request, user)
            return JsonResponse({'status': 'success', 'message': 'User registered successfully'}, status=200)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'}, status=405)

@csrf_exempt
def login_view(request):
    """
    API view to manage user login.
    """
    if request.method == 'POST':
        # Load JSON data from the request body
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Return JSON response on successful login
            return JsonResponse({'message': 'Login successful'}, status=200)
        else:
            # Return error message if authentication fails
            return JsonResponse({'error': 'Invalid username or password'}, status=400)

    # Return a JSON response for non-POST requests
    return JsonResponse({'error': 'Invalid request'}, status=400)

@csrf_exempt
def logout_view(request):
    """
    API view to handle user logout
    """
    auth_logout(request)
    return redirect('main_spa') #redirect


def article_list(request):
    """
    API view to display a list of news articles.
    """
    articles = list(Article.objects.values('id', 'title', 'category__name', 'author_name'))
    return JsonResponse({'articles': articles}, safe=False)

def article_detail(request, article_id):
    """
    API view to display the details of a single news article, including comments.
    """
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
    """
    API view to display a list of news articles filtered by user's favorite categories.
    """
    user = request.user
    favorite_categories = user.favorite_categories.all()
    articles = Article.objects.filter(category__in=favorite_categories).values('id', 'title', 'category__name', 'author_name')
    return JsonResponse({'articles': list(articles)}, safe=False)

def category_list(request):
    """
    API view to display a list of news categories.
    """
    categories = list(Category.objects.values('id', 'name'))
    return JsonResponse({'categories': categories}, safe=False)

def articles_by_category(request, category_id):
    """
    API view to display articles belonging to a specific category.
    """
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
        if request.content_type == 'application/json':
            # Handle JSON data
            data = json.loads(request.body)
            user.email = data.get('email', user.email)
            user.birth_date = data.get('birth_date', user.birth_date)
            if 'favorite_categories' in data:
                favorite_categories = data['favorite_categories']
                user.favorite_categories.set(favorite_categories)
        elif request.FILES.get('profile_image'):
            # Handle file upload
            file = request.FILES['profile_image']
            file_name = default_storage.save(file.name, file)
            user.profile_image = file_name

        user.save()
        return JsonResponse({'message': 'Profile updated successfully'})

    else:
        return HttpResponse(status=405)  # Method Not Allowed

@csrf_exempt
@login_required
def post_comment(request, article_id, parent_comment_id=None):
    """
    API view for posting a comment on a news article or replying to a comment.
    """
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
    """
    API view to edit an existing comment.
    """
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
    """
    API view to delete an existing comment.
    """
    if request.method == 'DELETE':
        comment = get_object_or_404(Comment, id=comment_id, author=request.user)
        comment.delete()
        return JsonResponse({'message': 'Comment deleted successfully'})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
