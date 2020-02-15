from django.urls import path
from my_api.api import Tag, Category, Article, Comment

urlpatterns = [
    path('tag_add', Tag.TagAdd.as_view()),
    path('tag_del', Tag.TagDel.as_view()),
    path('tag_update', Tag.TagUpdate.as_view()),
    path('tag_list', Tag.TagList.as_view()),
    path('category_add', Category.CategoryAdd.as_view()),
    path('category_del', Category.CategoryDel.as_view()),
    path('category_update', Category.CategoryUpdate.as_view()),
    path('category_list', Category.CategoryList.as_view()),
    path('article_add', Article.ArticleAdd.as_view()),
    path('article_del', Article.ArticleDel.as_view()),
    path('article_update', Article.ArticleUpdate.as_view()),
    path('article_list', Article.ArticleList.as_view()),
    path('article_details', Article.ArticleDetails.as_view()),
    path('comment_add', Comment.CommentAdd.as_view()),
    path('comment_list', Comment.CommentList.as_view())
]
