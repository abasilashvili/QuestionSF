from django.urls import path
from .views import Post, PostDetailView, PostListView
from .views import NewsCreate, ArticleCreate,NewsUpdate, ArticleUpdate,NewsDelete, ArticleDelete
from .views import NewsListView, ArticleListView
from . import views
from .views import IndexView



urlpatterns = [

    path('', NewsListView.as_view(), name='news_list'),
    path('news/create/', NewsCreate.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('article/create/', ArticleCreate.as_view(), name='article_create'),
    path('article/<int:pk>/edit/', ArticleUpdate.as_view(), name='article_update'),
    path('article/<int:pk>/delete/', ArticleDelete.as_view(), name='article_delete'),
    path('news/', NewsListView.as_view(), name='news_list'),
    path('article/', ArticleListView.as_view(), name='article_list'),
    path("news/<int:pk>/", views.news_detail, name="news_detail"),
    path("article/<int:pk>/", views.article_detail, name="article_detail"),
]