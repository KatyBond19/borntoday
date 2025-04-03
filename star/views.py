from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from datetime import date, timedelta
from .models import Star, Country, Category
from django.contrib import messages
from django.shortcuts import redirect
from .forms import StarForm

def index(request):
    """
    Главная страница: выводим все звёзды + выделяем, у кого сегодня/завтра/послезавтра день рождения.
    """
    # Получаем все опубликованные звезды
    all_stars = Star.objects.filter(is_published=True)

    # Получаем текущую дату
    today = date.today()
    tomorrow = today + timedelta(days=1)
    day_after_tomorrow = today + timedelta(days=2)

    # Находим звезд с днями рождения
    today_stars = []
    tomorrow_stars = []
    day_after_tomorrow_stars = []

    for star in all_stars:
        # Проверяем месяц и день (без учета года)
        if star.birth_date.month == today.month and star.birth_date.day == today.day:
            today_stars.append(star)
        elif star.birth_date.month == tomorrow.month and star.birth_date.day == tomorrow.day:
            tomorrow_stars.append(star)
        elif star.birth_date.month == day_after_tomorrow.month and star.birth_date.day == day_after_tomorrow.day:
            day_after_tomorrow_stars.append(star)

    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': all_stars,
        'today_stars': today_stars,
        'tomorrow_stars': tomorrow_stars,
        'day_after_tomorrow_stars': day_after_tomorrow_stars,
        'today_date': today,
        'tomorrow_date': tomorrow,
        'day_after_tomorrow_date': day_after_tomorrow,
        'star_countries': countries,
        'star_categories': categories,
        'title': 'Дни рождения звезд'
    }
    return render(request, 'star/index.html', context)


def star_detail(request, slug):
    """
    Детальная страница конкретной звезды: /person/<slug>/
    """
    # Получаем объект звезды по slug или выбрасываем 404 ошибку
    star = get_object_or_404(Star, slug=slug, is_published=True)

    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'star': star,
        'star_countries': countries,
        'star_categories': categories,
    }

    return render(request, 'star/star_detail.html', context)


def about(request):
    """
    Страница «О сайте».
    """
    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'title': 'О сайте',
        'description': '"Borntoday" — это уникальный ресурс, посвященный дням рождения знаменитостей. Здесь вы найдете информацию о том, кто из известных людей празднует день рождения сегодня, а также сможете узнать интересные факты из их жизни, карьеры и творчества.',
        'star_countries': countries,
        'star_categories': categories,
    }
    return render(request, 'star/about.html', context)


def stars_by_country(request, slug):
    country = get_object_or_404(Country, slug=slug)
    filtered_stars = Star.objects.filter(country=country, is_published=True)

    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': filtered_stars,
        'country_name': country.name,
        'star_countries': countries,
        'star_categories': categories,
        'title_template': 'Знаменитости из страны'
    }
    return render(request, 'star/country.html', context)


def stars_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    filtered_stars = Star.objects.filter(categories=category, is_published=True)

    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'stars': filtered_stars,
        'category_name': category.title,
        'star_countries': countries,
        'star_categories': categories,
        'title_template': 'Знаменитости из отрасли',
    }
    return render(request, 'star/industry.html', context)



def add_star(request):
    """
    Представление для добавления новой знаменитости
    """
    if request.method == 'POST':
        form = StarForm(request.POST, request.FILES)
        if form.is_valid():
            star = form.save(commit=False)
            star.is_published = True
            star.save()
            form.save_m2m()  # Сохраняем связи many-to-many
            messages.success(request, f'Знаменитость "{star.name}" успешно добавлена!')
            return redirect('star_detail', slug=star.slug)
    else:
        form = StarForm()

    # Получаем все страны и категории для меню
    countries = Country.objects.all()
    categories = Category.objects.all()

    context = {
        'form': form,
        'title': 'Добавление знаменитости',
        'star_countries': countries,
        'star_categories': categories,
    }
    return render(request, 'star/add_star.html', context)



RUSSIAN_ALPHABET = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ'

def get_alphabet_context():
    # Получаем буквы, на которые есть знаменитости
    existing_letters = []
    for letter in RUSSIAN_ALPHABET:
        if Star.objects.filter(is_published=True, name__istartswith=letter).exists():
            existing_letters.append(letter)

    return {
        'alphabet': RUSSIAN_ALPHABET,
        'existing_letters': existing_letters
    }


def sitemap(request):
    stars = Star.objects.filter(is_published=True).order_by('name')
    context = {
        'stars': stars,
        'star_countries': Country.objects.all(),
        'star_categories': Category.objects.all(),
        'title': 'Карта сайта'
    }
    context.update(get_alphabet_context())
    return render(request, 'star/sitemap.html', context)


def sitemap_letter(request, letter):
    letter = letter.upper()  # Приводим к верхнему регистру
    stars = Star.objects.filter(
        is_published=True,
        name__istartswith=letter
    ).order_by('name')

    context = {
        'stars': stars,
        'current_letter': letter,
        'star_countries': Country.objects.all(),
        'star_categories': Category.objects.all(),
        'title': f'Знаменитости на букву {letter}',
    }
    context.update(get_alphabet_context())
    return render(request, 'star/sitemap_letter.html', context)


def about(request):
    # Получаем статистику
    stats = {
        'stars': Star.objects.filter(is_published=True).count(),
        'countries': Country.objects.count(),
        'categories': Category.objects.count(),
    }

    context = {
        'title': 'О сайте',
        'stats': stats,
        # Другие данные контекста, если есть
    }
    return render(request, 'star/about.html', context)