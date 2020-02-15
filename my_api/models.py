from django.db import models


class User(models.Model):
    """
    客户端用户
    """
    user_name = models.CharField(max_length=20, verbose_name='用户名')
    user_email = models.EmailField(verbose_name='用户邮箱')

    def __str__(self):
        return self.user_name


class Tag(models.Model):
    """
    标签
    """
    tag_name = models.CharField(max_length=20, verbose_name='标签名称')
    tag_alias = models.CharField(max_length=20,
                                 blank=True,
                                 null=True,
                                 verbose_name='标签别名')
    tag_desc = models.CharField(max_length=100,
                                blank=True,
                                null=True,
                                verbose_name='标签描述')

    def __str__(self):
        return self.tag_name


class Category(models.Model):
    """
    分类
    """
    sort_num = models.IntegerField(default=0, verbose_name='排序')
    category_name = models.CharField(max_length=20, verbose_name='分类名称')
    category_alias = models.CharField(max_length=20,
                                      blank=True,
                                      null=True,
                                      verbose_name='分类别名')
    category_desc = models.CharField(max_length=100,
                                     blank=True,
                                     null=True,
                                     verbose_name='分类描述')
    parent_category_id = models.IntegerField(default=-1, verbose_name='父分类id')

    # 重写__str__方法，在admin后台遇到该对象，会展示该方法返回的值
    def __str__(self):
        return self.category_name


class Article(models.Model):
    """
    文章
    """
    article_title = models.CharField(max_length=50, verbose_name='标题')
    article_content = models.TextField(blank=True,
                                       null=True,
                                       verbose_name='内容')
    article_views = models.IntegerField(default=0, verbose_name='浏览数')
    comment_content = models.IntegerField(default=0, verbose_name='评论总数')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='发布日期')
    update_date = models.DateTimeField(auto_now=True, verbose_name='修改日期')
    # 多对一
    category = models.ForeignKey(Category,
                                 on_delete=models.DO_NOTHING,
                                 related_name='articles',
                                 verbose_name='文章分类')
    # 多对多
    tags = models.ManyToManyField(Tag,
                                  related_name='articles',
                                  verbose_name='文章标签')

    def __str__(self):
        return self.article_title


class Comment(models.Model):
    """
    留言
    """
    comment_content = models.TextField(verbose_name='留言内容')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='发布日期')
    # 多对一
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='comments',
                             verbose_name='留言用户')
    # 多对一
    article = models.ForeignKey(Article,
                                on_delete=models.CASCADE,
                                related_name='comments',
                                verbose_name='所属文章')

    def __str__(self):
        # str截取前10个字符串返回
        return self.comment_content[:10]
