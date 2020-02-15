from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from my_api import models, serializers


class CommentAdd(APIView):
    """
    新增留言
    """
    def post(self, request):
        comment_content = request.POST.get('comment_content')
        user_id = request.POST.get('user_id')
        user_name = request.POST.get('user_name')
        user_email = request.POST.get('user_email')
        article_id = request.POST.get('article_id')

        data = {"comment_content": comment_content, "article_id": article_id}

        # 如果user信息不为空，就直接使用；如果为空，那就创建一个新用户
        if user_id:
            # 用户信息不为空，就直接查找用户信息
            data['user_id'] = user_id
        elif user_name and user_email:
            # 用户信息为空，给定了用户名和用户邮箱，就创建一个新用户
            newUser = models.User(user_name=user_name, user_email=user_email)
            newUser.save()
            data['user_id'] = newUser.id
        else:
            return Response({"code": 200, "msg": "参数错误", "data": ""})

        ser_post_data = serializers.CommentSerializer(data=data)
        if ser_post_data.is_valid():
            ser_post_data.save()
            return Response({"code": 200, "msg": "success", "data": ""})
        return Response(ser_post_data.errors,
                        status=status.HTTP_400_BAD_REQUEST)


class CommentList(APIView):
    """
    留言列表
    """
    def post(self, request):
        article_id = request.POST.get('article_id')

        search_dict = {}
        if article_id:
            search_dict['article'] = article_id

        query_data = models.Comment.objects.filter(**search_dict)
        ser_query_data = serializers.CommentSerializer(query_data, many=True)
        return Response({
            "code": 200,
            "msg": "success",
            "data": ser_query_data.data
        })
