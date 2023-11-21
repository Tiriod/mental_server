import json

from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (Activity, Information, Book, ShareLoop, User, EmotionRecord, Food, Image, Emotion, Meditation,
                     Audio, Action, )


# 用户分享圈管理功能
class ShareLoopAdmin(admin.ModelAdmin):
    # 在列表中显示的字段: 用户名称, 用户心情, 发布时间
    list_display = ('shareloop_id', 'username', 'user_emotion', 'display_base64_image_list', 'release_time')
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

    @staticmethod
    def display_base64_image(obj):
        # 获取图像 Base64 数据
        image_id = obj.information_image_id

        # 如果有数据，在HTML中显示
        if image_id:
            base64_data = Image.objects.get(image_id=image_id).image_data
            # 添加标签，将Base64信息数据渲染为img图片类型
            image_html = format_html('<img src="{}" width="200px" height="auto"/>', base64_data)
            return mark_safe(image_html)
        else:
            # 否则显示样式为无图片的样式
            return 'No Image'

    display_base64_image.short_description = 'Decoded Image'


# 图片表管理功能
class ImageAdmin(admin.ModelAdmin):
    # 显示列
    list_display = ('image_id', 'display_base64_image')
    # 词条数量
    list_per_page = 10
    # 搜索内容
    search_fields = ('image_id',)

    def display_base64_image(self, obj):
        # 获取图像 Base64 数据
        base64_data = obj.image_data
        # 如果有数据，在HTML中显示
        if base64_data:
            # 添加标签，将Base64信息数据渲染为img图片类型
            image_html = format_html('<img src="{}" width="200px" height="auto"/>', base64_data)
            return mark_safe(image_html)
        else:
            # 否则显示样式为无图片的样式
            return 'No Image'

    display_base64_image.short_description = 'Decoded Image'


# 食品表管理功能
class FoodAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'food_name', 'food_image_id', 'display_base64_image', 'quantity', 'calories')
    # 直接编辑food_image_id
    list_editable = ('food_image_id',)  # 允许在列表页面直接编辑 food_image_id
    # 词条数量
    list_per_page = 10

    @staticmethod
    def display_base64_image(obj):
        # 获取与当前 Food 对象关联的图片 ID
        image_id = obj.food_image_id
        # 如果有图片 ID，则查询对应的 Image 记录
        if image_id:
            try:
                image = Image.objects.get(image_id=image_id)
                base64_data = image.image_data
                # 如果有数据，在 HTML 中显示
                if base64_data:
                    # 添加标签，将 Base64 信息数据渲染为 img 图片类型
                    image_html = format_html('<img src="{}" width="50px" height="auto"/>', base64_data)
                    return mark_safe(image_html)
            except Image.DoesNotExist:
                pass
        return 'No Image'


# 书目管理后台
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_type', 'display_base64_image', 'book_copy_writing', 'book_heading')
    # 词条数量
    list_per_page = 10

    @staticmethod
    def display_base64_image(obj):
        # 获取与当前 Food 对象关联的图片 ID
        image_id = obj.book_image_id
        # 如果有图片 ID，则查询对应的 Image 记录
        if image_id:
            try:
                image = Image.objects.get(image_id=image_id)
                # 如果有数据，在 HTML 中显示
                if image.image_data:
                    # 添加标签，将 Base64 信息数据渲染为 img 图片类型
                    image_html = format_html('<img src="{}" width="50px" height="auto"/>', image.image_data)
                    return mark_safe(image_html)
            except Image.DoesNotExist:
                pass
        return 'No Image'


# 用户管理后台
class UserAdmin(admin.ModelAdmin):
    list_display = ('display_base64_image', 'username', 'iphone', 'description')
    search_fields = ('username',)
    list_editable = ('iphone', 'description')
    # 词条数量
    list_per_page = 10

    @staticmethod
    def display_base64_image(obj):
        # 获取与当前 User 对象关联的图片 ID
        image_id = obj.user_avatar_id
        # 如果有图片 ID，则查询对应的 Image 记录
        if image_id:
            try:
                image = Image.objects.get(image_id=image_id)
                base64_data = image.image_data
                # 如果有数据，在 HTML 中显示
                if base64_data:
                    # 添加标签，将 Base64 信息数据渲染为 img 图片类型
                    image_html = format_html('<img src="{}" width="100px" height="auto"/>', base64_data)
                    return mark_safe(image_html)
            except Image.DoesNotExist:
                pass
        return 'No Image'


class MeditationAdmin(admin.ModelAdmin):
    list_display = ('meditation_id', 'meditation_type', 'meditation_name', 'display_base64_image', 'play', 'audio_id')

    @staticmethod
    def display_base64_image(obj):
        image_id = obj.meditation_image_id
        if image_id:
            try:
                image = Image.objects.get(image_id=image_id)
                base64_data = image.image_data
                # 如果有数据，在 HTML 中显示
                if base64_data:
                    # 添加标签，将 Base64 信息数据渲染为 img 图片类型
                    image_html = format_html('<img src="{}" style="width: 100px; height: auto; margin: '
                                             '5px; border-radius: 5px;" />', base64_data)
                    return mark_safe(image_html)
            except Image.DoesNotExist:
                pass
        return 'No Image'

    display_base64_image.short_description = 'Meditation Cover'


class AudioAdmin(admin.ModelAdmin):
    list_display = ('audio_id', 'audio_file')


# 管理员页面注册表
admin.site.register(Activity)
admin.site.register(Information, InformationAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(ShareLoop, ShareLoopAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(EmotionRecord)
admin.site.register(Food, FoodAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Emotion)
admin.site.register(Meditation, MeditationAdmin)
admin.site.register(Audio, AudioAdmin)
admin.site.register(Action)
