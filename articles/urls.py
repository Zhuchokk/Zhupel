from django.urls import path
from . import views

app_name = 'articles'
urlpatterns = [
    path('', views.index, name="index"),
    path('article/<int:id>/', views.one_article, name="one_article"),
    path('article/<str:theme>/', views.theme_articles, name="theme_articles"),
    path('themes', views.theme_view, name="theme_view"),
    path('article/like/<int:id>&<str:key>&<int:value>', views.like_register, name="like_register"),
    path('article/comment/<int:id>&<str:key>&<int:value>', views.comment_register, name="comment_register"),
]
