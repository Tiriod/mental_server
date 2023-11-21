from django.contrib import admin
from django.urls import path
from mental_app import views

app_name = 'mental_app'

urlpatterns = [
    # 活动API
    path('api/v1/activities/', views.ActivityListView.as_view(), name='activity-list'),
    # 资讯API
    path('api/v1/information/', views.InformationListView.as_view(), name='information-list'),
    # 书目API
    path('api/v1/books/', views.BookListView.as_view(), name='book-list'),
    # 分享圈API
    path('api/v1/shareloops/', views.ShareLoopListView.as_view(), name='shareloop-list'),
    path('api/v1/shareloops/upload/', views.shareloops_upload, name="shareloop-upload"),
    # 用户API
    path('api/v1/users/', views.UserListView.as_view(), name='user-list'),
    # 心绪记录API
    path('api/v1/emotionrecords/', views.EmotionRecordListView.as_view(), name='emotionrecord-list'),
    # 食物地址API
    path('api/v1/foods/', views.FoodListView.as_view(), name='food-list'),
    # 图像上传API
    path('api/v1/image/upload/', views.image_upload, name="image_upload"),
    # 冥想音频API
    path('api/v1/meditations/', views.MeditationListView.as_view(), name="meditations-list"),
    path('api/v1/meditations/<int:meditation_id>/', views.MeditationListView.as_view(), name='meditation-detail'),
    # 管理员API
    path('admin/', admin.site.urls),
]
