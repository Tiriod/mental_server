import json

from rest_framework import serializers
from .models import Activity, Information, Book, ShareLoop, User, EmotionRecord, Food, Image, Emotion, Meditation, \
    Audio, Action, TestModule


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = '__all__'


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ShareLoopSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShareLoop
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class EmotionRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmotionRecord
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # 将 action_list 由字符串转换为列表
        action_list_str = representation.get('action_list', '[]')
        try:
            action_list = json.loads(action_list_str)
            representation['action_list'] = action_list
        except json.JSONDecodeError:
            # 如果解析失败，保持原始的字符串形式
            pass

        return representation


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class EmotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emotion
        fields = '__all__'


class MeditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meditation
        fields = '__all__'


class AudioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Audio
        fields = '__all__'


class ActionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Action
        fields = '__all__'


class TestModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TestModule
        fields = 'all'

