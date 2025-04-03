from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='star_index'),  # Главная страница
    path('person/<slug:slug>/', views.star_detail, name='star_detail'),  # Детальная страница

    # Страница «О сайте»
    path('about/', views.about, name='about'),

    # Знаменитости по стране
    path('country/<slug:slug>/', views.stars_by_country, name='stars_by_country'),

    # Знаменитости по виду деятельности
    path('industry/<slug:slug>/', views.stars_by_category, name='stars_by_category'),

    path('add/', views.add_star, name='add_star'),

    path('sitemap/', views.sitemap, name='sitemap'),

    path('sitemap/<str:letter>/', views.sitemap_letter, name='sitemap_letter'),

]