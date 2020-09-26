from dal import autocomplete
from django.urls import path

from archives.models import InfoBase
from . import views
from .feeds import LatestArticlesFeed

app_name = 'articles'
urlpatterns = [
    path('', views.ArticlesList.as_view(), name='all_articles'),
    path('like/', views.article_like, name='like'),
    path('create_article/', views.CreateArticle.as_view(), name='create_article'),
    path('search/', views.article_search, name='article_search'),
    path('bookmark_article/', views.bookmark_article, name='bookmark_article'),
    path('item_autocomplete/', autocomplete.Select2QuerySetView.as_view(model=InfoBase), name='item_autocomplete'),
    path('<int:comment_id>/update_comment/', views.edit_comment, name='edit_comment'),
    path('<int:comment_id>/delete_comment/', views.delete_comment, name='delete_comment'),
    path('<int:comment_id>/reply_comment/', views.reply_comment, name='reply_comment'),
    path('<int:article_id>/create_comment/', views.create_comment, name='create_comment'),
    path('<slug:slug>/update_article/', views.UpdateArticle.as_view(),
         name='update_article'),
    path('<slug:slug>/delete_article/', views.DeleteArticle.as_view(),
         name='delete_article'),
    path('<slug:slug>/', views.article_detail, name='article_detail'),
    path('<int:article_id>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.ArticlesList.as_view(), name='all_articles_by_tag'),
    path('feed/', LatestArticlesFeed(), name='article_feed'),
]
