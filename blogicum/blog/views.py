from django.shortcuts import get_object_or_404, render
# Можно лучше:
# При использовании часового пояса отличного от UTC, будет
# выскакивать warning, поэтому лучше заменить время на это
# from django.utils import timezone и использовать timezone вместо datetime.
from django.utils import timezone

from core.constants import POSTS_BY_PAGE
from .models import Category, Post


# Надо исправить:
# Вызов now() на уровне модуля недопустим.
# POSTS = Post.objects.filter(..., pub_date__lt=now(),) Так делать нельзя.
# NOW = now()

# Надо исправить:
# Выносим повторяющийся код в функцию.
# Можно лучше:
# Можно рассказать про менеджеры моделей и queryset и вынести туда.
def get_published_posts():
    """Возвращает queryset опубликованных постов."""
    return Post.objects.select_related(
        'author', 'category', 'location'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )


def index(request):
    posts = get_published_posts()[:POSTS_BY_PAGE]
    return render(request, 'blog/index.html', {'posts': posts})


def post_detail(request, post_id):
    post = get_object_or_404(
        Post,
        pk=post_id,
        is_published=True,
        category__is_published=True,
        pub_date__lte=timezone.now()
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )
    posts = get_published_posts().filter(category=category)
    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts
    })