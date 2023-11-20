from rest_framework.response import Response
from rest_framework import generics, status
from django.http import JsonResponse
from .models import Activity, Information, Book, ShareLoop, User, EmotionRecord, Food
from .serializers import (
    ActivitySerializer,
    InformationSerializer,
    BookSerializer,
    ShareLoopSerializer,
    UserSerializer,
    EmotionRecordSerializer,
    FoodSerializer,
)
from rest_framework.decorators import api_view


# 活动表单信息
class ActivityListView(generics.ListAPIView):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


# AI资讯表单信息
class InformationListView(generics.ListAPIView):
    queryset = Information.objects.all()
    serializer_class = InformationSerializer


# 书目表单信息
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# 分享圈表单信息
class ShareLoopListView(generics.ListAPIView):
    queryset = ShareLoop.objects.all()
    serializer_class = ShareLoopSerializer


# 用户表单信息
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 心情记录表单信息
class EmotionRecordListView(generics.ListAPIView):
    queryset = EmotionRecord.objects.all()
    serializer_class = EmotionRecordSerializer


# 食品表单信息
class FoodListView(generics.ListAPIView):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


@api_view(["POST"])
def api_test(request):
    received_data = request.query_params.get('test_text')

    # 构造要返回的 JSON 数据
    response_data = {
        "status": "success",
        "message": "Data received successfully",
        "test_text": received_data
    }
    return JsonResponse(response_data, status=status.HTTP_200_OK)


@api_view(["POST"])
def shareLoop_upload(request):
    # 发布用户的id信息
    user_id = request.data.get('user_id')
    # 用户心情信息
    user_emotion = request.data.get('user_emotion')
    # 用户分享圈文案信息
    shareLoop_copy_writing = request.data.get('shareLoop_copy_writing')
    # 用户图像列表
    image_list = request.FILES.get('image_list')
    # 上传时间
    release_time = request.data.get('release_time')

    # 构造要返回的 JSON 数据
    response_data = {
        "status": "success",
        "message": "Data received successfully",
        "data": {
            "user_id": user_id,
            "user_emotion": user_emotion,
            "shareLoop_copy_writing": shareLoop_copy_writing,
            "image_list": image_list,
            "release_time": release_time
        }
    }

    # 在数据库中创建 ShareLoop 实例
    serializer = ShareLoopSerializer(data=response_data['data'])
    if serializer.is_valid():
        serializer.save()

    return JsonResponse(response_data, status=status.HTTP_200_OK)
