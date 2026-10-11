from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Article, Category

class BlogTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Создаем обычного пользователя, второго пользователя (для проверки прав) и админа
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='testpassword')
        self.admin_user = User.objects.create_superuser(username='adminuser', password='testpassword')
        
        # Создаем категорию и статью
        self.category = Category.objects.create(name='Новости')
        self.article = Article.objects.create(
            title='Тестовая статья',
            content='Текст тестовой статьи',
            author=self.user,
            category=self.category
        )

    #тесты моделей
    
    def test_article_creation(self):
        # Проверяем, что статья успешно создалась с правильными связями
        self.assertEqual(self.article.title, 'Тестовая статья')
        self.assertEqual(self.article.author.username, 'testuser')
        self.assertEqual(self.article.category.name, 'Новости')
        
    def test_model_string_representations(self):
        # Проверяем методы __str__ у моделей
        self.assertEqual(str(self.category), 'Новости')
        self.assertEqual(str(self.article), 'Тестовая статья')

    #тесты отображения страниц

    def test_article_list_view(self):
        # Проверяем, что главная страница загружается и содержит тестовую статью
        response = self.client.get(reverse('article_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая статья')

    def test_article_detail_view(self):
        # Проверяем страницу конкретной статьи
        response = self.client.get(reverse('article_detail', args=[self.article.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Текст тестовой статьи')

    #тесты прав доступа и авторизации

    def test_article_create_requires_login(self):
        # Проверяем, что анонимного пользователя перекидывает на страницу входа
        response = self.client.get(reverse('article_create'))
        self.assertNotEqual(response.status_code, 200)
        self.assertTrue(response.url.startswith('/login/'))

    def test_only_author_can_edit_article(self):
        # Логинимся под другим пользователем
        self.client.login(username='otheruser', password='testpassword')
        response = self.client.get(reverse('article_update', args=[self.article.pk]))
        
        # Код во views.py должен запретить доступ и перенаправить его на главную
        self.assertEqual(response.status_code, 302) 
        self.assertEqual(response.url, reverse('article_list'))

    def test_only_admin_can_create_category(self):
        # Логинимся под обычным пользователем и пытаемся создать категорию
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('category_create'))
        
        self.assertEqual(response.status_code, 302)

        # логинимся под админом
        self.client.login(username='adminuser', password='testpassword')
        response_admin = self.client.get(reverse('category_create'))
        
        # Ожидаем успешную загрузку страницы
        self.assertEqual(response_admin.status_code, 200)

    #тесты фильтрации и поиска

    def test_search_by_title(self):
        # Ищем существующую статью
        response = self.client.get(reverse('article_list'), {'title': 'Тестовая'})
        self.assertContains(response, 'Тестовая статья')
        
        # Ищем несуществующую статью
        response_empty = self.client.get(reverse('article_list'), {'title': 'Абракадабра'})
        self.assertNotContains(response_empty, 'Тестовая статья')
        self.assertContains(response_empty, 'Статей по вашему запросу не найдено.')