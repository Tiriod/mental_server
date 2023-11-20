from django.contrib import admin
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import (Activity, Information, Book, ShareLoop, User, EmotionRecord, Food, Image, Emotion, Meditation,
                     Audio, Action, )


# 用户分享圈管理功能
class ShareLoopAdmin(admin.ModelAdmin):
    # 在列表中显示的字段: 用户名称, 用户心情, 发布时间
    list_display = ('user_id', 'user_emotion', 'release_time')
    # 启用搜索功能，搜索'user_emotion'字段
    search_fields = ('user_emotion',)
    # 启用过滤器，按照发布时间进行过滤
    list_filter = ('release_time',)
    # 自定义动作示例
    actions = ['make_published']

    def make_published(self, queryset):
        queryset.update(status='published')

    make_published.short_description = "标记为已发布"


# 资讯表管理功能
class InformationAdmin(admin.ModelAdmin):
    list_display = ('information_id', 'information_heading', 'information_image_id')


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

    @staticmethod
    def display_base64_image(obj):
        # 获取与当前 Food 对象关联的图片 ID
        image_id = obj.book_image_id
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


# 管理员页面注册表
admin.site.register(Activity)
admin.site.register(Information, InformationAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(ShareLoop, ShareLoopAdmin)
admin.site.register(User)
admin.site.register(EmotionRecord)
admin.site.register(Food, FoodAdmin)
admin.site.register(Image, ImageAdmin)
admin.site.register(Emotion)
admin.site.register(Meditation)
admin.site.register(Audio)
admin.site.register(Action)
