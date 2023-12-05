import base64
import base64
import json
import pickle
import time

import pandas
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseServerError
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response

import Utils.DateUtil
from .models import Activity, Information, Book, ShareLoop, User, EmotionRecord, Food, Image, Meditation, Emotion, \
    TestModule, Audio, Action
from .serializers import (ActivitySerializer, InformationSerializer, BookSerializer, ShareLoopSerializer,
                          UserSerializer, EmotionRecordSerializer, FoodSerializer, ImageSerializer,
                          MeditationSerializer, EmotionSerializer, TestModuleSerializer, AudioSerializer,
                          ActionSerializer)


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


@csrf_exempt
def get_book_type(request, book_type):
    # 使用 filter 获取满足条件的所有书籍对象
    books = Book.objects.filter(book_type=book_type)
    # 序列化书籍对象列表
    serializer = BookSerializer(books, many=True)
    # 获取序列化后的数据
    response_data = serializer.data
    return JsonResponse(response_data, safe=False)


class ShareLoopListView(generics.ListCreateAPIView):
    """用户分享圈信息"""
    queryset = ShareLoop.objects.all()
    serializer_class = ShareLoopSerializer


# 心情分享圈POST上传
@csrf_exempt
def shareLoops_upload(request):
    if request.method == "POST":
        data = json.loads(request.body)

        # 用户名称
        username = data.get("username")
        print("Username:", username)
        # 用户心情
        user_emotion = data.get("user_emotion")
        # 文案信息
        shareLoop_copy_writing = data.get("shareLoop_copy_writing")

        # 获取上传的文件列表
        uploaded_images = data.get("image_list", [])
        print(uploaded_images)

        image_id_list = []
        for image_data in uploaded_images:
            image_id = add_image_base64(image_data)
            image_id_list.append(image_id)

        # 添加时间
        release_time = timezone.now()  # 使用带时区信息的当前时间
        # 创建 ShareLoop 记录
        ShareLoop.objects.create(
            username=username,
            user_emotion=user_emotion,
            shareLoop_copy_writing=shareLoop_copy_writing,
            image_id_list=json.dumps(image_id_list),  # 将图像ID列表转为JSON字符串
            release_time=release_time
        )

        # 构建要返回的JSON数据
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

    else:
        return JsonResponse({"error": "Invalid method."})


class UserListView(generics.ListAPIView):
    """用户表单信息"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        user_id = self.kwargs.get('user_id')
        # 通过meditation查询的情况
        if username:
            try:
                USER = User.objects.get(username=username)
                # 返回获取到的数据
                serializer = UserSerializer(USER)
                return JsonResponse(serializer.data)
            except User.DoesNotExist:
                return JsonResponse({'detail': 'User not found'})

        if user_id:
            # 如果包含冥想的类型（meditation_type），返回符合条件的冥想信息
            try:
                USER = User.objects.get(user_id=user_id)
                # 返回获取到的数据
                serializer = UserSerializer(USER)
                return JsonResponse(serializer.data)
            except User.DoesNotExist:
                return JsonResponse({'detail': 'User not found'})
        else:
            # 否则返回所有的冥想信息
            queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@csrf_exempt
def user_upload(request):
    if request.method == 'POST':
        # 使用 request.body 获取原始的 JSON 数据
        username = request.POST.get('username')
        password = request.POST.get('password')
        phone = request.POST.get('phone')
        if phone:
            # 创建新的心绪记录表
            User.objects.create(
                username=username,
                password=password,
                iphone=phone
            )
        else:
            # 创建新的心绪记录表
            User.objects.create(
                username=username,
                password=password
            )
        return JsonResponse({"status": "success"})


# 上传EmotionRecord的信息
@csrf_exempt
def emotionRecord_upload(request):
    if request.method == 'POST':
        # 使用 request.body 获取原始的 JSON 数据
        data = json.loads(request.body.decode('utf-8'))
        user_id = data.get('user_id')
        emotion_text = data.get('emotion_text')
        action_list = data.get('action_list')

        # 获取对应用户的实例，如果找不到返回404响应
        user_instance = get_object_or_404(User, user_id=user_id)

        # 添加时间
        release_time = timezone.now()  # 使用带时区信息的当前时间
        # 将时间格式化为字符串
        formatted_time = release_time.strftime("%Y-%m-%dT%H:%M:%S")

        # 创建新的心绪记录表
        emotion_record = EmotionRecord.objects.create(
            user_id=user_instance,
            emotion_text=emotion_text,
            release_time=formatted_time,
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


# 食物信息
def food_statistics():
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
        'id': food_ids,
        'type': food_types,
        'food_imageIDList': food_imageIDList,
        'food_name': food_name,
        'calories': calories,
    }
    return response_data


# 食物推荐
@csrf_exempt
def breakfast_meal(request):
    food_data = food_statistics()
    # 将JSON数据转换为DataFrame
    food_df = pandas.DataFrame(food_data)
    # 根据热量需求筛选食物
    filtered_data = food_df[food_df['calories'] <= 400]
    # 按类型随机选择一种食物
    selected_type = "肉蛋奶"
    selected_food = filtered_data[filtered_data['type'] == selected_type].sample(2)
    selected_type = "主食"
    selected_food2 = filtered_data[filtered_data['type'] == selected_type].sample(1)
    # 将两个选择的食物合并成一个列表
    result_list = selected_food.to_dict('records') + selected_food2.to_dict('records')
    # 使用JsonResponse返回结果
    return JsonResponse({"recommended_meal": result_list})


# 食物推荐
@csrf_exempt
def lunch_meal(request):
    food_data = food_statistics()
    # 将JSON数据转换为DataFrame
    food_df = pandas.DataFrame(food_data)
    # 根据热量需求筛选食物
    filtered_data = food_df[food_df['calories'] <= 600]
    # 按类型随机选择一种食物
    selected_type = "主食"
    selected_food = filtered_data[filtered_data['type'] == selected_type].sample(1)
    selected_type = "肉蛋奶"
    selected_food2 = filtered_data[filtered_data['type'] == selected_type].sample(2)
    selected_type = "蔬果"
    selected_food3 = filtered_data[filtered_data['type'] == selected_type].sample(2)
    selected_type = "坚果"
    selected_food4 = filtered_data[filtered_data['type'] == selected_type].sample(1)
    # 将两个选择的食物合并成一个列表
    result_list = selected_food.to_dict('records') + selected_food2.to_dict('records') + selected_food3.to_dict(
        'records') + selected_food4.to_dict('records')
    # 使用JsonResponse返回结果
    return JsonResponse({"recommended_meal": result_list})


# 食物推荐
@csrf_exempt
def dinner_meal(request):
    food_data = food_statistics()
    # 将JSON数据转换为DataFrame
    food_df = pandas.DataFrame(food_data)
    # 根据热量需求筛选食物
    filtered_data = food_df[food_df['calories'] <= 400]
    # 按类型随机选择一种食物
    selected_type = "主食"
    selected_food = filtered_data[filtered_data['type'] == selected_type].sample(1)
    selected_type = "肉蛋奶"
    selected_food2 = filtered_data[filtered_data['type'] == selected_type].sample(1)
    selected_type = "蔬果"
    selected_food3 = filtered_data[filtered_data['type'] == selected_type].sample(2)
    # 将两个选择的食物合并成一个列表
    result_list = selected_food.to_dict('records') + selected_food2.to_dict('records') + selected_food3.to_dict(
        'records')
    # 使用JsonResponse返回结果
    return JsonResponse({"recommended_meal": result_list})


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


def add_image_base64(base64_data):
    time.sleep(1)
    image_id = Utils.DateUtil.get_image_id()
    Image.objects.create(image_id=image_id, image_data=base64_data)
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
                return JsonResponse(serializer.data)
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


@csrf_exempt
def model_test(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question_list = data.get('question_list')
            option_list = data.get('option_list')

            if question_list is None or option_list is None:
                return HttpResponseBadRequest("Invalid JSON data: 'question_list' and 'option_list' are required.")

            ans = ''
            # 进行决策
            for i in range(len(question_list)):
                tree = load_decision_tree("mental_server/model/测一测决策树.pkl")
                result = make_decision(tree, question_list[i], option_list[i])
                ans += result

            # 打印结果
            return JsonResponse({"result": ans})

        except json.JSONDecodeError as e:
            print("Error decoding JSON:", str(e))
            return HttpResponseBadRequest("Invalid JSON data")

        except Exception as e:
            print("Error processing request:", str(e))
            return HttpResponseServerError("Internal Server Error")

    return HttpResponseBadRequest("Invalid request method")


class AudioModuleListView(generics.ListAPIView):
    """测一测模块表单信息"""
    queryset = TestModule.objects.all()
    serializer_class = AudioSerializer


@csrf_exempt
def get_audio(request, audio_id):
    audio_instance = get_object_or_404(Audio, audio_id=audio_id)

    # 使用序列化器将图片实例序列化为JSON数据
    serializer = AudioSerializer(audio_instance)
    # 获取 Base64 数据
    base64_data = serializer.data.get('audio_data', '')
    # 在这里添加其他数据处理逻辑，然后构建要返回的JSON数据
    response_data = {
        'status': 'success',
        'message': 'Image data retrieved successfully',
        'image_id': audio_instance.audio_id,
        'base64_data': base64_data,
    }
    return JsonResponse(response_data)


class ActionListView(generics.ListAPIView):
    """行为表单信息"""
    queryset = Action.objects.all()
    serializer_class = ActionSerializer


@csrf_exempt
def get_action(request, action_id):
    # 获取对应图片的实例，如果找不到返回404响应
    ACTION = get_object_or_404(Action, action_id=action_id)
    # 使用序列化器将图片实例序列化为JSON数据
    serializer = ActionSerializer(ACTION)
    # 在这里添加其他数据处理逻辑，然后构建要返回的JSON数据
    response_data = serializer.data
    return JsonResponse(response_data)
