from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from my_api import models, serializers


class CategoryAdd(APIView):
    """
    新增分类
    """
    def post(self, request):
        ser_post_data = serializers.CategorySerializer(data=request.data)
        if ser_post_data.is_valid():
            ser_post_data.save()
            return Response({"code": 200, "msg": "success", "data": ""})
        return Response(ser_post_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CategoryDel(APIView):
    """
    删除分类
    """
    def post(self, request):
        id = request.POST.get('id')
        if not id:
            return Response({"code": 200, "msg": "参数错误！", "data": ""})
        try:
            query_data = models.Category.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"code": 200, "msg": "不存在！", "data": ""})
        query_data.delete()
        return Response({"code": 200, "msg": "success", "data": ""})


class CategoryUpdate(APIView):
    """
    更新分类
    """
    def post(self, request):
        id = request.POST.get('id')
        if not id:
            return Response({"code": 200, "msg": "参数错误！", "data": ""})
        try:
            targetObj = models.Category.objects.get(id=id)
        except ObjectDoesNotExist:
            return Response({"code": 200, "msg": "不存在！", "data": ""})
        ser_post_data = serializers.CategorySerializer(data=request.data)
        if ser_post_data.is_valid():
            ser_post_data.update(instance=targetObj,
                                 validated_data=request.data)
            return Response({"code": 200, "msg": "success", "data": ""})
        return Response(ser_post_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CategoryList(APIView):
    """
    分类列表
    """
    def post(self, request):
        query_data = models.Category.objects.all()
        ser_query_data = serializers.CategorySerializer(query_data, many=True)
        return Response({
            "code": 200,
            "msg": "success",
            "data": ser_query_data.data
        })
