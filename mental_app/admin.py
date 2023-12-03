import json

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (Activity, Information, Book, ShareLoop, User, EmotionRecord, Food, Image, Emotion, Meditation,
                     Audio, Action, TestModule)


# admin页面显示图像方法

def display_base64_image(image_id):
    try:
        image = Image.objects.get(image_id=image_id)
        base64_data = image.image_data

        if base64_data:
            image_html = format_html(
                '<img src="{}" style="width: auto; height: 50px; margin-right: 10px; border-radius: 5px;"/>',
                base64_data)
            return mark_safe(image_html)
    except Image.DoesNotExist:
        print(f"Image with image_id={image_id} not found.")

    return 'No Image'


# 用户分享圈管理功能
class ShareLoopAdmin(admin.ModelAdmin):
    # 在列表中显示的字段: 用户名称, 用户心情, 发布时间
    list_display = ('shareLoop_id', 'username', 'user_emotion', 'display_base64_image_list', 'release_time')
    # 启用搜索功能，搜索'user_emotion'字段
    search_fields = ('user_emotion',)
    # 启用过滤器，按照发布时间进行过滤
    list_filter = ('release_time',)
    # 自定义动作示例
    actions = ['make_published']
    # 词条数量
    list_per_page = 5

    def display_base64_image_list(self, obj):
        try:
            # 将JSON字符串转换为实际的Python列表
            image_id_list = json.loads(obj.image_id_list)
            # 过滤掉空字符串
            image_id_list = [image_id.strip() for image_id in image_id_list if image_id.strip()]
        except json.JSONDecodeError:
            print("Error decoding image_id_list JSON.")
            image_id_list = []
        # HTML图像渲染内容
        images_html = []
        if image_id_list:
            for image_id in image_id_list:
                try:
                    base64_data = Image.objects.get(image_id=image_id).image_data
                    images_html.append(format_html('<img src="{}" style="width: 50px; height: auto; margin: '
                                                   '5px; border-radius: 5px;"/>', base64_data))
                except Image.DoesNotExist:
                    print(f"Image with image_id={image_id} not found.")
            return mark_safe(''.join(images_html))
        else:
            return 'No Image'

    display_base64_image_list.short_description = 'Decoded Image'


# 资讯表管理功能
class InformationAdmin(admin.ModelAdmin):
    list_display = ('information_id', 'information_heading', 'display_base64_image')
    # 词条数量
    list_per_page = 5

    def display_base64_image(self, obj):
        return display_base64_image(obj.information_image_id)

    display_base64_image.short_description = 'Decoded Image'


# 食品表管理功能
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'food_name', 'food_image_id', 'display_base64_image', 'quantity', 'calories')
    # 直接编辑type
    list_editable = ('type',)  # 允许在列表页面直接编辑 type
    # 词条数量
    list_per_page = 20
    # 词条搜索内容
    search_fields = ('type',)

    def display_base64_image(self, obj):
        return display_base64_image(obj.food_image_id)

    display_base64_image.short_description = 'Decoded Image'


# 图片表管理功能
class ImageAdmin(admin.ModelAdmin):
    # 显示列
    list_display = ('image_id', 'display_base64_image')
    # 词条数量
    list_per_page = 20
    # 搜索内容
    search_fields = ('image_id',)

    def display_base64_image(self, obj):
        return display_base64_image(obj.image_id)

    display_base64_image.short_description = 'Decoded Image'


# 书目管理后台
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_type', 'display_base64_image', 'book_copy_writing', 'book_heading')
    # 词条数量
    list_per_page = 10

    def display_base64_image(self, obj):
        return display_base64_image(obj.book_image_id)

    display_base64_image.short_description = 'Decoded Image'


# 用户管理后台
class UserAdmin(admin.ModelAdmin):
    list_display = ('display_base64_image', 'username', 'iphone', 'description')
    search_fields = ('username',)
    list_editable = ('iphone', 'description')
    # 词条数量
    list_per_page = 10

    def display_base64_image(self, obj):
        return display_base64_image(obj.user_avatar_id)

    display_base64_image.short_description = 'Decoded Image'


class EmotionAdmin(admin.ModelAdmin):
    list_display = ('emotion_id', 'emotion_image_id', 'display_base64_image', 'emotion_text')

    def display_base64_image(self, obj):
        return display_base64_image(obj.emotion_image_id)

    display_base64_image.short_description = 'Decoded Image'


class MeditationAdmin(admin.ModelAdmin):
    list_display = ('meditation_id', 'meditation_type', 'meditation_name', 'display_base64_image', 'play', 'audio_id')

    def display_base64_image(self, obj):
        return display_base64_image(obj.meditation_image_id)

    display_base64_image.short_description = 'Decoded Image'


class AudioAdmin(admin.ModelAdmin):
    list_display = ('audio_id', 'audio_file', 'audio_data')
    list_editable = ('audio_data',)


class ActionAdmin(admin.ModelAdmin):
    list_display = ('action_id', 'action_image_id', 'display_base64_image', 'action_text',)

    def display_base64_image(self, obj):
        return display_base64_image(obj.action_image_id)

    display_base64_image.short_description = 'Decoded Image'


# 心绪记录表单
class EmotionRecordAdmin(admin.ModelAdmin):
    list_display = ('record_id', 'user_id', 'emotion_text', 'action_list', 'release_time')


class TestModuleAdmin(admin.ModelAdmin):
    list_display = ('test_id', 'display_base64_image', 'test_question', 'test_choiceA', 'test_choiceB', 'test_choiceC')

    def display_base64_image(self, obj):
        return display_base64_image(obj.test_image_id)

    display_base64_image.short_description = 'Decoded Image'


# 管理员页面装饰器
admin.site.register(Activity)
admin.site.register(Information, InformationAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(ShareLoop, ShareLoopAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Food, FoodAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Emotion, EmotionAdmin)
admin.site.register(Meditation, MeditationAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(EmotionRecord, EmotionRecordAdmin)
admin.site.register(TestModule, TestModuleAdmin)
