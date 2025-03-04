from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),
    path('articole/', views.all_articles, name='all_articles'),
    path('articol/<slug:slug>/', views.article_detail, name='article_detail'),
    path('categorie/<slug:slug>/', views.category_articles, name='category_articles'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('calculator-bmi/', views.bmi_calculator, name='bmi_calculator'),
]
