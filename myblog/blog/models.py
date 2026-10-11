from django.db import models
from django.contrib.auth.models import User

# Модель для групп статей
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название группы")

    def __str__(self):
        return self.name

# Модель для самой статьи
class Article(models.Model):
    title = models.CharField(max_length=250, verbose_name="Название статьи")
    content = models.TextField(verbose_name="Текст статьи")
    # дата автоматически
    date_published = models.DateField(auto_now_add=True, verbose_name="Дата публикации")
    
    #связь с пользователями
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    # связь с катеориями
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Группа")

    def __str__(self):
        return self.title