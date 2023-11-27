from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from .models import Article, Comment, User, Category
from django.views.decorators.csrf import csrf_exempt
import json


def main_spa(request: HttpRequest) -> HttpResponse:
    return render(request, 'api/spa/index.html', {})

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
    """
    API view for the user's profile page. Handles both viewing and updating the profile.
    """
    user = request.user
    if request.method == "GET":
        user_data = {
            'username': user.username,
            'email': user.email,
            'birth_date': user.birth_date,
            'profile_image': user.profile_image.url if user.profile_image else None
        }
        return JsonResponse(user_data)
    elif request.method == "POST":
        data = json.loads(request.body)
        user.email = data.get('email', user.email)
        user.birth_date = data.get('birth_date', user.birth_date)
        # Handle profile image update here if necessary
        user.save()
        return JsonResponse({'message': 'Profile updated successfully'})

@csrf_exempt
@login_required
def post_comment(request, article_id):
    """
    API view for posting a comment on a news article.
    """
    if request.method == "POST":
        article = get_object_or_404(Article, id=article_id)
        data = json.loads(request.body)
        comment_content = data.get('comment')
        Comment.objects.create(article=article, author=request.user, content=comment_content)
        return JsonResponse({'message': 'Comment added successfully'})

