from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Article, Category
from .forms import ArticleForm, RegisterForm, CategoryForm

#главная страница:список статей и поиск
def article_list(request):
    articles = Article.objects.all()
    categories = Category.objects.all()
    
    # Получаем данные из параметров поиска
    query_title = request.GET.get('title', '')
    query_author = request.GET.get('author', '')
    query_date = request.GET.get('date', '')
    query_category = request.GET.get('category', '')

    # Простые фильтры для поиска
    if query_title:
        articles = articles.filter(title__icontains=query_title)
    if query_author:
        articles = articles.filter(author__username__icontains=query_author)
    if query_date:
        articles = articles.filter(date_published=query_date)
    if query_category:
        articles = articles.filter(category_id=query_category)

    #переменные запроса в контекст
    context = {
        'articles': articles,
        'categories': categories,
        'query_title': query_title,
        'query_author': query_author,
        'query_date': query_date,
        'query_category': query_category,
    }
    return render(request, 'blog/article_list.html', context)

# Чтение одной статьи
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'blog/article_detail.html', {'article': article})

# Создание статьи, только для авторизованных
@login_required
def article_create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user # Автором становится текущий пользователь
            article.save()
            return redirect('article_list')
    else:
        form = ArticleForm()
    return render(request, 'blog/article_form.html', {'form': form})

# Редактирование статьи
@login_required
def article_update(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    if article.author != request.user:
        return redirect('article_list')
        
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleForm(instance=article)
    return render(request, 'blog/article_form.html', {'form': form})

@login_required
def article_delete(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    if article.author != request.user:
        return redirect('article_list')
        
    if request.method == 'POST':
        article.delete()
        return redirect('article_list')
    return render(request, 'blog/article_confirm_delete.html', {'article': article})

@login_required
def category_create(request):
    if not request.user.is_superuser:
        return redirect('article_list')
        
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_create')
    else:
        form = CategoryForm()
    return render(request, 'blog/category_form.html', {'form': form, 'categories': categories})

@login_required
def category_update(request, pk):
    if not request.user.is_superuser:
        return redirect('article_list')
        
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_create')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'blog/category_form.html', {'form': form})

@login_required
def category_delete(request, pk):
    if not request.user.is_superuser:
        return redirect('article_list')
        
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_create')
    return render(request, 'blog/category_confirm_delete.html', {'category': category})

def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('article_list')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form': form})

def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('article_list')
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('article_list')