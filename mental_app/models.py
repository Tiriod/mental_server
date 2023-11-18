from django.db import models


class Activity(models.Model):
    """活动表"""
    activity_id = models.AutoField(primary_key=True)  # 活动id
    activity_heading = models.CharField(max_length=255)  # 活动标题
    activity_image_id = models.CharField(max_length=100)  # 活动图片地址
    activity_description = models.TextField()  # 活动描述


class Information(models.Model):
    """资讯表"""
    information_id = models.AutoField(primary_key=True)  # 资讯id
    information_heading = models.CharField(max_length=255)  # 资讯标题
    information_image_id = models.CharField(max_length=100)  # 资讯图片id
    information_copy_writing = models.TextField()  # 资讯内容
    information_date = models.DateField()  # 资讯时间
    information_source = models.CharField(max_length=255)  # 资讯来源


class Book(models.Model):
    """书本表"""
    book_id = models.AutoField(primary_key=True)  # 书目id
    book_type = models.CharField(max_length=255)  # 书目类型
    book_image_id = models.CharField(max_length=100)  # 书目图片地址
    book_copy_writing = models.TextField()  # 书目正文
    book_heading = models.CharField(max_length=255)  # 书目标题名称


class ShareLoop(models.Model):
    """分享圈表单"""
    user_id = models.AutoField(primary_key=True)  # 用户id
    user_emotion = models.CharField(max_length=255)  # 用户心情
    shareLoop_copy_writing = models.TextField()  # 文本信息
    image_list_id = models.CharField(max_length=100)  # 图片列表ID
    release_time = models.DateTimeField()  # 发布时间


class User(models.Model):
    """用户表"""
    user_id = models.AutoField(primary_key=True)  # 用户id
    user_avatar_id = models.CharField(max_length=100)  # 用户头像图像地址
    username = models.CharField(max_length=255)  # 用户名
    password = models.CharField(max_length=255)  # 用户密码
    iphone = models.CharField(max_length=20, null=True, blank=True)  # 用户手机号(允许为空)
    description = models.CharField(max_length=100, null=True, blank=True)  # 用户自我描述(允许为空)


class Action(models.Model):
    """行为表"""
    action_id = models.AutoField(primary_key=True)  # 行为id
    action_image_id = models.CharField(max_length=100)  # 行为图标地址
    action_text = models.CharField(max_length=10)  # 行为文本


class EmotionRecord(models.Model):
    """情绪记录表"""
    record_id = models.AutoField(primary_key=True)  # 记录id
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)  # 用户id
    emotion_text = models.TextField()  # 用户心情
    release_time = models.DateTimeField()  # 记录时间
    action_list = models.ManyToManyField(Action)  # 活动行为列表


class Food(models.Model):
    """食物表"""
    id = models.AutoField(primary_key=True)  # 食物id
    type = models.CharField(max_length=255)  # 食物类型
    food_image_id = models.CharField(max_length=100)  # 食物图片地址
    food_name = models.CharField(max_length=255)  # 食物名称
    quantity = models.IntegerField(default=100)  # 食物质量
    calories = models.IntegerField()  # 食物卡路里


class Image(models.Model):
    """图像表"""
    image_id = models.CharField(max_length=100, primary_key=True)  # 图像ID
    image_data = models.TextField()  # 图像Base64数据信息


class Emotion(models.Model):
    """表情表"""
    emotion_id = models.AutoField(primary_key=True)  # 表情id
    emotion_image_id = models.CharField(max_length=100)  # 表情图像地址
    emotion_text = models.CharField(max_length=255)  # 表情名称


class Meditation(models.Model):
    """冥想音频表单"""
    meditation_id = models.AutoField(primary_key=True)  # 冥想id
    meditation_name = models.CharField(max_length=100)  # 冥想名称
    meditation_image_id = models.CharField(max_length=100)  # 图片地址
    play = models.IntegerField()  # 播放量
    audio_id = models.CharField(max_length=100)  # 音频内容地址


class Audio(models.Model):
    """音频表"""
    audio_id = models.CharField(max_length=100, primary_key=True)  # 音频特征id
    audio_data = models.TextField()  # 音频存储信息
