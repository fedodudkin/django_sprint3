import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogicum.blogicum.settings')
django.setup()

from django.contrib.auth import get_user_model
from blog.models import Category, Location, Post
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

# Создаем тестового пользователя
user, created = User.objects.get_or_create(
    username='testuser',
    defaults={'email': 'test@example.com'}
)
if created:
    user.set_password('password123')
    user.save()

# Создаем категории
cat1, _ = Category.objects.get_or_create(
    title='Технологии',
    defaults={'slug': 'tech', 'description': 'Посты о технологиях'}
)
cat2, _ = Category.objects.get_or_create(
    title='Наука',
    defaults={'slug': 'science', 'description': 'Научные посты'}
)

# Создаем локации
loc1, _ = Location.objects.get_or_create(name='Москва')
loc2, _ = Location.objects.get_or_create(name='Санкт-Петербург')

# Создаем посты
for i in range(5):
    Post.objects.get_or_create(
        title=f'Тестовый пост {i+1}',
        defaults={
            'text': f'Это текст тестового поста номер {i+1}. ' * 10,
            'author': user,
            'category': cat1 if i % 2 == 0 else cat2,
            'location': loc1 if i % 2 == 0 else loc2,
            'pub_date': timezone.now() - timedelta(hours=i),
            'is_published': True
        }
    )

print(f'Created {Post.objects.count()} posts')
