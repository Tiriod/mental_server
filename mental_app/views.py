import base64
import json
import time
from urllib.parse import unquote

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

import Utils.DateUtil
from .models import Activity, Information, Book, ShareLoop, User, EmotionRecord, Food, Image, Meditation, Emotion
from .serializers import (ActivitySerializer, InformationSerializer, BookSerializer, ShareLoopSerializer,
                          UserSerializer, EmotionRecordSerializer, FoodSerializer, ImageSerializer,
                          MeditationSerializer, EmotionSerializer)


class ActivityListView(generics.ListAPIView):
    """活动表单信息"""
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer


class InformationListView(generics.ListAPIView):
    """AI资讯表单信息"""
    queryset = Information.objects.all()
    serializer_class = InformationSerializer


class BookListView(generics.ListAPIView):
    """书目表单信息"""
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ShareLoopListView(generics.ListCreateAPIView):
    """用户分享圈信息"""
    queryset = ShareLoop.objects.all()
    serializer_class = ShareLoopSerializer


@csrf_exempt
def shareloops_upload(request):
    if request.method == 'POST':
        # 用户名称
        username = request.POST.get('username')
        # 用户心情
        user_emotion = request.POST.get('user_emotion')
        # 文案信息
        shareloop_copy_writing = request.POST.get('shareloop_copy_writing')
        # 提取图像数据列表
        uploaded_images = request.FILES.getlist('image_list')
        # 添加时间
        release_time = request.POST.get('release_time')
        # 保存每个图像数据到 Image 表，并构建 image_id 列表
        image_id_list = []
        for uploaded_image in uploaded_images:
            image_id_list.append(image_storage(uploaded_image))
            time.sleep(1)
        # 创建返回的数据库表单
        # 创建 ShareLoop 记录
        ShareLoop.objects.create(
            username=username,
            user_emotion=user_emotion,
            shareloop_copy_writing=shareloop_copy_writing,
            image_id_list=json.dumps(image_id_list),  # 将图像ID列表转为JSON字符串
            release_time=release_time
        )
        # 在这里添加其他数据处理逻辑，然后构建要返回的JSON数据
        response_data = {
            'status': 'success',
            'message': 'Data received successfully',
            'username': username,
            'user_emotion': user_emotion,
            'shareloop_copy_writing': shareloop_copy_writing,
            'image_id_list': image_id_list,
            'release_time': release_time
            # 在这里添加其他数据字段
        }
        return JsonResponse(response_data)
    return JsonResponse({'status': 'error！', 'message': 'Hi！Guys, the request method is wrong, it is POST, not GET!'})


class UserListView(generics.ListAPIView):
    """用户表单信息"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class EmotionRecordListView(generics.ListAPIView):
    """心情记录表单信息"""
    queryset = EmotionRecord.objects.all()
    serializer_class = EmotionRecordSerializer


class FoodListView(generics.ListAPIView):
    """食品表单信息"""
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class ImageListView(generics.ListAPIView):
    """图像信息表"""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


# 图像上传方法: 此处的image_data应当为base64的数据格式
def add_image(image_data, image_format='jpeg'):
    # 获取特征性 image_id
    image_id = Utils.DateUtil.get_image_id()
    # 在 Image 数据库表单内创建一条新的 image_data 数据信息
    base64_data = f'data:image/{image_format};base64,{image_data}'
    Image.objects.create(image_id=image_id, image_data=base64_data)
    # 返回特征性的 image_id
    return image_id


# 图像上传(文件上传)
@csrf_exempt
def image_upload(request):
    if request.method == 'POST':
        # 获取上传的图片
        uploaded_image = request.FILES.get('image_data')
        image_format = uploaded_image.name.split('.')[-1].lower()
        # 添加图片到 Image 表并获取 image_id
        base64_data = base64.b64encode(uploaded_image.read()).decode('utf-8')
        image_id = add_image(base64_data, image_format)

        # 构造返回的 JSON 数据
        response_data = {
            'status': 'success',
            'message': 'Data received successfully',
            'image_id': image_id,
        }
        return JsonResponse(response_data)
    return JsonResponse({'status': 'error！', 'message': 'Hi！Guys, the request method is wrong, it is POST, not GET!'})


def image_storage(image):
    # 将Image数据转为base64编码形式
    data = base64.b64encode(image.read()).decode('utf-8')
    # 获取image的图片类型
    image_format = image.name.split('.')[-1].lower()
    # 获取存储image后得到的id信息
    image_id = add_image(data, image_format)
    return image_id


class MeditationListView(generics.ListAPIView):
    """冥想信息表"""
    queryset = Meditation.objects.all()
    serializer_class = MeditationSerializer

    def get(self, request, *args, **kwargs):
        meditation_id = self.kwargs.get('meditation_id')
        meditation_type = self.kwargs.get('meditation_type')

        if meditation_id:
            # 如果包含冥想的主键（meditation_id），将播放量加一
            try:
                meditation = Meditation.objects.get(meditation_id=meditation_id)
                meditation.play += 1
                meditation.save()
                # 返回获取到的数据
                serializer = MeditationSerializer(meditation)
                return JsonResponse(serializer.data)
            except Meditation.DoesNotExist:
                return Response({'detail': 'Meditation not found'}, status=status.HTTP_404_NOT_FOUND)

        if meditation_type:
            # 如果包含冥想的类型（meditation_type），返回符合条件的冥想信息
            queryset = self.filter_queryset(self.get_queryset().filter(meditation_type__icontains=meditation_type))
        else:
            # 否则返回所有的冥想信息
            queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmotionListView(generics.ListAPIView):
    """心情信息表"""
    queryset = Emotion.objects.all()
    serializer_class = EmotionSerializer

    # get方法
    def get(self, request, *args, **kwargs):
        emotion_text = self.kwargs.get('emotion_text')
        emotion_id = self.kwargs.get('emotion_id')
        if emotion_text:
            try:
                # 通过emotion_text来获取对应的emotion内容
                emotion = Emotion.objects.get(emotion_text=emotion_text)
                serializer = EmotionSerializer(emotion)  # 使用你的序列化器
                return JsonResponse({'result': serializer.data})
            except Meditation.DoesNotExist:
                return Response({'detail': 'Meditation not found'}, status=status.HTTP_404_NOT_FOUND)
        if emotion_id:
            try:
                # 通过emotion_text来获取对应的emotion内容
                emotion = Emotion.objects.get(emotion_id=emotion_id)
                serializer = EmotionSerializer(emotion)  # 使用你的序列化器
                return JsonResponse({'result': serializer.data})
            except Meditation.DoesNotExist:
                return Response({'detail': 'Meditation not found'}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({'status': 'error！', 'message': 'Nothing'})
