from django.urls import path
from . import views
from django.views.generic import RedirectView

app_name = 'articles'
urlpatterns = [
    path('', views.index, name="index"),
    path('article/<int:id>/', views.one_article, name="one_article"),
    path('article/<str:theme>/', views.theme_articles, name="theme_articles"),
    path('themes', views.theme_view, name="theme_view"),
    path(r'^favicon\.ico$', RedirectView.as_view(url='/static//images/favicon.ico'), name='favicon'),
]
