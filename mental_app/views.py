import ast
import base64
import datetime
import json
import pickle
import time

import jieba
import pandas
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

import Utils.DateUtil
from .models import Activity, Information, Book, ShareLoop, User, EmotionRecord, Food, Image, Meditation, Emotion, \
    TestModule
from .serializers import (ActivitySerializer, InformationSerializer, BookSerializer, ShareLoopSerializer,
                          UserSerializer, EmotionRecordSerializer, FoodSerializer, ImageSerializer,
                          MeditationSerializer, EmotionSerializer, TestModuleSerializer)


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


# 心情分享圈POST上传
@csrf_exempt
def shareLoops_upload(request):
    # 用户名称
    username = request.POST.get('username')
    # 用户心情
    user_emotion = request.POST.get('user_emotion')
    # 文案信息
    shareLoop_copy_writing = request.POST.get('shareLoop_copy_writing')
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
        shareloop_copy_writing=shareLoop_copy_writing,
        image_id_list=json.dumps(image_id_list),  # 将图像ID列表转为JSON字符串
        release_time=release_time
    )
    # 在这里添加其他数据处理逻辑，然后构建要返回的JSON数据
    response_data = {
        'status': 'success',
        'message': 'Data received successfully',
        'username': username,
        'user_emotion': user_emotion,
        'shareLoop_copy_writing': shareLoop_copy_writing,
        'image_id_list': image_id_list,
        'release_time': release_time
        # 在这里添加其他数据字段
    }
    return JsonResponse(response_data)


class UserListView(generics.ListAPIView):
    """用户表单信息"""
    queryset = User.objects.all()
    serializer_class = UserSerializer


# 上传EmotionRecord的信息
@csrf_exempt
def emotionRecord_upload(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        emotion_text = request.POST.get('emotion_text')
        release_time = request.POST.get('release_time')
        action_list_str = request.POST.get('action_list')

        # 获取对应用户的实例，如果找不到返回404响应
        user_instance = get_object_or_404(User, user_id=user_id)

        # 将 action_list_str 转换为 Python 列表
        try:
            action_list = json.loads(action_list_str)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format for action_list'})

        # 创建新的心绪记录表
        emotion_record = EmotionRecord.objects.create(
            user_id=user_instance,
            emotion_text=emotion_text,
            release_time=release_time,
            action_list=action_list,
        )
        # 在这里添加其他数据处理逻辑，然后构建要返回的JSON数据
        response_data = {
            'status': 'success',
            'message': 'Data received successfully',
            'user_id': str(emotion_record.user_id.pk),  # 使用.pk获取用户主键
            'emotion_text': emotion_record.emotion_text,
            'release_time': emotion_record.release_time,
            'action_list': emotion_record.action_list,
        }
        return JsonResponse(response_data)
    return JsonResponse({'status': 'error', 'message': 'Hi! Guys, the request method is wrong, it is GET, not POST!'})


# 查询单个用户的心情信息数据
@csrf_exempt
def emotionRecord_user(request, user_id):
    USER = get_object_or_404(User, user_id=user_id)
    emotionRecords = EmotionRecord.objects.filter(user_id=USER)
    serializer = EmotionRecordSerializer(emotionRecords, many=True)

    # 提取每个记录的 'emotion_text' 字段
    emotion_texts = [record['emotion_text'] for record in serializer.data]
    # 在这里添加其他数据处理逻辑，然后构建要返回的JSON数据
    response_data = {
        'status': 'success',
        'message': 'Emotion records retrieved successfully',
        'user_id': USER.user_id,
        'emotion_records': emotion_texts,
    }
    return JsonResponse(response_data)


class FoodListView(generics.ListAPIView):
    """食品表单信息"""
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


@csrf_exempt
def food_Details(request, food_name):
    # 获取对应食品的实例，如果找不到返回404响应
    food = get_object_or_404(Food, food_name=food_name)

    serializer = FoodSerializer(food)

    # 在这里添加其他数据处理逻辑，然后构建要返回的JSON数据
    response_data = {
        'status': 'success',
        'message': 'Food details retrieved successfully',
        'food_details': serializer.data,
    }
    return JsonResponse(response_data)


# 智能获取食物信息
@csrf_exempt
def food_Statistics(request):
    foods = Food.objects.all()
    serializer = FoodSerializer(foods, many=True)
    # 从序列化结果中提取所需的信息，这里假设 Food 模型有相应的字段，你可以根据实际情况修改
    food_ids = [food['id'] for food in serializer.data]
    food_types = [food['type'] for food in serializer.data]
    food_imageIDList = [food['food_image_id'] for food in serializer.data]
    food_name = [food['food_name'] for food in serializer.data]
    calories = [food['calories'] for food in serializer.data]
    # 构建返回的字典
    response_data = {
        'status': 'success',
        'id': food_ids,
        'type': food_types,
        'food_imageIDList': food_imageIDList,
        'food_name': food_name,
        'calories': calories,
    }
    if request.method == 'GET':
        return JsonResponse(response_data)  # 返回 JSON 响应
    elif request.method == 'POST':
        return response_data  # 直接返回字典


# 食物推荐
@csrf_exempt
def food_Recommendations(request):
    food_data_response = food_Statistics(request)
    food_data = json.loads(food_data_response.content)

    # 将 'calories' 列表中的每个元素转换为字符串
    food_data['calories'] = [str(calorie) for calorie in food_data['calories']]

    # 将类型和卡路里拼接为一个文本
    food_data['features'] = [' '.join([type_, str(calorie)]) for type_, calorie in
                             zip(food_data['type'], food_data['calories'])]

    # 中文分词
    food_data['features'] = [' '.join(jieba.cut(x)) for x in food_data['features']]

    # 使用 TF-IDF 向量化食物的特征
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(food_data['features'])

    # 计算余弦相似度
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

    # 获取食物名称到索引的映射
    def get_recommendations(food_name, top_n=4):
        idx = pandas.Series(range(len(food_data['food_name'])), index=food_data['food_name']).drop_duplicates()[
            food_name]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1: top_n + 1]  # 取前4个相似的食物
        food_indices = [i[0] for i in sim_scores]
        return [food_data['food_name'][i] for i in food_indices]

    Date = datetime.datetime.now()
    DAY = Date.day
    # 示例：获取与某个食物相似的推荐
    response_data = {
        'status': 'success',
        'message': 'Image data retrieved successfully',
        'breakfast': get_recommendations(food_data['food_name'][DAY - 7], 4),
        'lunch': get_recommendations(food_data['food_name'][DAY], 6),
        'dinner': get_recommendations(food_data['food_name'][DAY + 7], 5),
    }
    return JsonResponse(response_data)


class ImageListView(generics.ListAPIView):
    """图像信息表"""
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


# 获取图像Base64数据
@csrf_exempt
def get_image_base64(request, image_id):
    # 获取对应图片的实例，如果找不到返回404响应
    image_instance = get_object_or_404(Image, image_id=image_id)
    # 使用序列化器将图片实例序列化为JSON数据
    serializer = ImageSerializer(image_instance)
    # 获取 Base64 数据
    base64_data = serializer.data.get('image_data', '')
    # 在这里添加其他数据处理逻辑，然后构建要返回的JSON数据
    response_data = {
        'status': 'success',
        'message': 'Image data retrieved successfully',
        'image_id': image_instance.image_id,
        'base64_data': base64_data,
    }
    return JsonResponse(response_data)


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
    return JsonResponse({'status': 'error', 'message': 'Hi! Guys, the request method is wrong, it is GET, not POST!'})


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
        # 通过meditation查询的情况
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


class EmotionRecordListView(generics.ListAPIView):
    """心绪记录表单信息"""
    queryset = EmotionRecord.objects.all()
    serializer_class = EmotionRecordSerializer


class TestModuleListView(generics.ListAPIView):
    """测一测模块表单信息"""
    queryset = TestModule.objects.all()
    serializer_class = TestModuleSerializer


# 加载决策树
def load_decision_tree(file_path):
    with open(file_path, "rb") as file:
        loaded_tree = pickle.load(file)
    return loaded_tree


# 进行决策树决策
def make_decision(decision_tree, current_question, selected_option):
    try:
        result = decision_tree[current_question][selected_option]
        return result
    except KeyError:
        return "未知结果"


# 决策树模型调用
@csrf_exempt
def test_model(request):
    if request.method == 'POST':
        question_list = request.POST.get('question_list')
        question_list = json.loads(question_list)
        option_list = request.POST.get('option_list')
        option_list = json.loads(option_list)
        ans = ''
        # 进行决策
        for i in range(len(question_list)):
            tree = load_decision_tree("mental_server/model/测一测决策树.pkl")
            result = make_decision(tree, question_list[i], option_list[i])
            ans += result
        # 打印结果
        return JsonResponse({"result": ans})
