from django.contrib import admin

from my_api.models import User, Tag, Category, Article, Comment

admin.site.register(User)
admin.site.register(Tag)
admin.site.register(Category)
admin.site.register(Article)
admin.site.register(Comment)
