from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path("", views.index, name="home"),
     path('about/', views.about, name='about'),
     path('contact/', views.contact, name='contact'),
    path("products/", views.product_list, name="product_list"),
    path("products/<slug:slug>/", views.product_detail, name="product_detail"),
    path("news/", views.news_list, name="news"),
    path("news/<slug:slug>/", views.news_detail, name="news_detail"),
]
# Custom error handlers
handler404 = "mainapp.views.custom_404_view"