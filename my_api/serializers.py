from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from my_api.models import User, Tag, Category, Article, Comment


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    parent_category_id = serializers.IntegerField(required=False)

    class Meta:
        model = Category
        fields = '__all__'


class ArticleSerializer(serializers.ModelSerializer):
    # 定义一个category_id，查找出对应分类的id
    category_id = serializers.IntegerField(source='category.id')
    create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',
                                            read_only=True)
    update_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',
                                            read_only=True)

    class Meta:
        # 指定序列化的表
        model = Article
        # 指定查找深度0-10
        depth = 1
        # 排除不序列化的字段,这是一个元祖逗号结尾
        exclude = ("category", "article_content")
        # 序列化所有数据，与exclude不能并存
        # fields="__all__"

    # 重写create方法，处理自定义逻辑
    def create(self, validated_data):
        try:
            validated_data['category'] = Category.objects.get(
                id=validated_data['category']['id'])
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("没有找到该分类")
        return Article.objects.create(**validated_data)


class ArticleDetailsSerializer(serializers.ModelSerializer):
    # 定义一个category_id，查找出对应分类的id
    category_id = serializers.IntegerField(source='category.id')
    create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',
                                            read_only=True)
    update_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',
                                            read_only=True)

    class Meta:
        # 指定序列化的表
        model = Article
        # 指定查找深度0-10
        depth = 1
        # 排除不序列化的字段,这是一个元祖逗号结尾
        exclude = ("category", )
        # 序列化所有数据，与exclude不能并存
        # fields="__all__"

    # 重写create方法，处理自定义逻辑
    def create(self, validated_data):
        try:
            validated_data['category'] = Category.objects.get(
                id=validated_data['category']['id'])
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("没有找到对象")
        return Article.objects.create(**validated_data)


class CommentSerializer(serializers.ModelSerializer):
    # user_id非必给的参数，如果有说明前端记录了用户信息，如果没有说明是新用户
    user_id = serializers.IntegerField(source='user.id', required=False)
    article_id = serializers.IntegerField(source='article.id')
    create_date = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S',
                                            read_only=True)

    user_name = serializers.CharField(source='user.user_name', read_only=True)
    user_email = serializers.EmailField(source='user.user_email',
                                        read_only=True)

    class Meta:
        model = Comment
        exclude = ("user", "article")

    def create(self, validated_data):
        try:
            validated_data['user'] = User.objects.get(
                id=validated_data['user']['id'])
            validated_data['article'] = Article.objects.get(
                id=validated_data['article']['id'])
        except ObjectDoesNotExist:
            raise ObjectDoesNotExist("没有找到对象")
        return Comment.objects.create(**validated_data)
