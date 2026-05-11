from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from blog.models import Category, Location, Post
from django.utils import timezone
from datetime import timedelta


class Command(BaseCommand):
    help = 'Create test data for the blog'

    def handle(self, *args, **options):
        User = get_user_model()

        # Создаем тестового пользователя
        user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))

        # Создаем категории
        cat1, _ = Category.objects.get_or_create(
            slug='tech',
            defaults={'title': 'Технологии', 'description': 'Посты о технологиях'}
        )
        cat2, _ = Category.objects.get_or_create(
            slug='science',
            defaults={'title': 'Наука', 'description': 'Научные посты'}
        )
        self.stdout.write(self.style.SUCCESS(f'Categories: {Category.objects.count()}'))

        # Создаем локации
        loc1, _ = Location.objects.get_or_create(name='Москва')
        loc2, _ = Location.objects.get_or_create(name='Санкт-Петербург')
        self.stdout.write(self.style.SUCCESS(f'Locations: {Location.objects.count()}'))

        # Создаем посты
        for i in range(5):
            post, created = Post.objects.get_or_create(
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
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created post: {post.title}'))

        self.stdout.write(self.style.SUCCESS(f'Total posts: {Post.objects.count()}'))
