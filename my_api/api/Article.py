from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from my_api import models, serializers


class ArticleAdd(APIView):
    """
    新增文章
    """
    def post(self, request):
        ser_post_data = serializers.ArticleSerializer(data=request.data)
        if ser_post_data.is_valid():
            ser_post_data.save()
            return Response({"code": 200, "msg": "success", "data": ""})
        return Response(ser_post_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ArticleDel(APIView):
    """
    文章删除
    """
    def post(self, request):
        id = request.POST.get('id')
        if not id:
            return Response({"code": 200, "msg": "参数错误！", "data": ""})
        try:
            query_data = models.Article.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"code": 200, "msg": "不存在！", "data": ""})
        query_data.delete()
        return Response({"code": 200, "msg": "success", "data": ""})


class ArticleUpdate(APIView):
    """
    文章更新
    """
    def post(self, request):
        id = request.POST.get('id')
        if not id:
            return Response({"code": 200, "msg": "参数错误！", "data": ""})
        try:
            targetObj = models.Article.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"code": 200, "msg": "不存在！", "data": ""})
        ser_post_data = serializers.ArticleSerializer(data=request.data)
        if ser_post_data.is_valid():
            ser_post_data.update(instance=targetObj,
                                 validated_data=request.data)
            return Response({"code": 200, "msg": "success", "data": ""})
        return Response(ser_post_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class ArticleList(APIView):
    """
    文章列表
    """
    def post(self, request):
        category_id = request.POST.get('category_id')
        tags_id = request.POST.get('tags_id')

        search_dict = {}
        if category_id:
            search_dict['category'] = category_id

        if tags_id:
            tags_id = tags_id.split(',')
        else:
            tags_id = []

        query_data = models.Article.objects.filter(**search_dict)
        if len(tags_id) > 0:
            query_data = []
            for item in models.Article.objects.filter(**search_dict):
                for item1 in item.tags.all():
                    if str(item1.id) in tags_id:
                        query_data.append(item)
                        # 发现了对象之后就终止循环，避免数据重复
                        break

        ser_query_data = serializers.ArticleSerializer(query_data, many=True)
        return Response({
            "code": 200,
            "msg": "success",
            "data": ser_query_data.data
        })


class ArticleDetails(APIView):
    """
    文章详情
    """
    def post(self, request):
        id = request.POST.get('id')
        if not id:
            return Response({"code": 200, "msg": "参数错误！", "data": ""})
        try:
            query_data = models.Article.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"code": 200, "msg": "不存在！", "data": ""})
        ser_query_data = serializers.ArticleDetailsSerializer(query_data)
        return Response({
            "code": 200,
            "msg": "success",
            "data": ser_query_data.data
        })
