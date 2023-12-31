from django.contrib import admin
from django.urls import path
from mental_app import views

app_name = 'mental_app'

urlpatterns = [
    # 活动 API
    path('api/v1/activities/', views.ActivityListView.as_view(), name='api-activity-list'),
    # 资讯 API
    path('api/v1/information/', views.InformationListView.as_view(), name='api-information-list'),
    # 书目 API
    path('api/v1/books/', views.BookListView.as_view(), name='api-book-list'),
    path('api/v1/books/<str:book_type>/', views.get_book_type, name='api-book-type'),
    # 分享圈 API
    path('api/v1/shareloops/', views.ShareLoopListView.as_view(), name='api-shareLoop-list'),
    path('api/v1/shareloops/upload/', views.shareLoops_upload, name='api-shareLoop-upload'),
    # 用户 API
    path('api/v1/users/', views.UserListView.as_view(), name='api-user-list'),
    path('api/v1/users/upload/', views.user_upload, name='api-user-upload'),
    path('api/v1/users/user_id/<int:user_id>/', views.UserListView.as_view(), name='api-get-user-information-by-id'),
    path('api/v1/users/username/<str:username>/', views.UserListView.as_view(),
         name='api-get-user-information-by-username'),
    # 心绪记录 API
    path('api/v1/emotionrecords/', views.EmotionRecordListView.as_view(), name='api-emotionRecord-list'),
    path('api/v1/emotionrecords/upload/', views.emotionRecord_upload, name='api-emotionRecords-upload'),
    path('api/v1/emotionrecords/<int:user_id>/', views.emotionRecord_user, name='api-emotionRecords-user'),
    # 食物地址 API
    path('api/v1/foods/', views.FoodListView.as_view(), name='api-food-list'),
    path('api/v1/foods/foodtistics/', views.food_Statistics, name='api-food-statistics'),
    path('api/v1/foods/recommend/breakfast/', views.breakfast_meal, name='api-food-recommendations'),
    path('api/v1/foods/recommend/lunch/', views.lunch_meal, name='api-food-recommendations'),
    path('api/v1/foods/recommend/dinner/', views.dinner_meal, name='api-food-recommendations'),
    path('api/v1/foods/fooddetails/<str:food_name>/', views.food_Details, name='api-food-details'),
    # 图像查询地址
    path('api/v1/images/', views.ImageListView.as_view(), name='api-image-get'),
    path('api/v1/images/<str:image_id>/', views.get_image_base64, name='get-image-base64'),
    # 图像上传 API
    path('api/v1/image/upload/', views.image_upload, name="api-image-upload"),
    # 冥想音频 API
    path('api/v1/meditations/', views.MeditationListView.as_view(), name="api-meditations-list"),
    path('api/v1/meditations/meditation_id/<int:meditation_id>/', views.MeditationListView.as_view(),
         name='api-meditations-id-detail'),
    path('api/v1/meditations/meditation_type/<str:meditation_type>/', views.MeditationListView.as_view(),
         name='api-meditations-type-detail'),
    # 音频文件获取
    path('api/v1/audio/<str:audio_id>/', views.get_audio, name='api-get-audio'),
    # 心情信息 API
    path('api/v1/emotion/emotion_text/<str:emotion_text>/', views.EmotionListView.as_view(),
         name='api-emotions-list-text'),
    path('api/v1/emotion/emotion_id/<int:emotion_id>/', views.EmotionListView.as_view(), name='api-emotions-list-id'),
    # “测一测”内容 API
    path('api/v1/testmodules/', views.TestModuleListView.as_view(), name='api-testModules'),
    path('api/v1/testmodules/model/', views.model_test, name='api-test-model'),
    # 获取单个用户信息
    # 行为信息 API
    path('api/v1/actions/', views.ActionListView.as_view(), name="api-actions"),
    path('api/v1/actions/<int:action_id>/', views.get_action, name="api-action"),
    # 管理员 API
    path('admin/', admin.site.urls, name='admin-site'),
]
