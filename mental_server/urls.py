"""
mental_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mental_app import views
from mental_app.views import (
    ActivityListView,
    InformationListView,
    BookListView,
    ShareLoopListView,
    UserListView,
    EmotionRecordListView,
    FoodListView,
)

urlpatterns = [
    # 活动API
    path('api/v1/activities/', ActivityListView.as_view(), name='activity-list'),
    # 资讯API
    path('api/v1/information/', InformationListView.as_view(), name='information-list'),
    # 书目API
    path('api/v1/books/', BookListView.as_view(), name='book-list'),
    # 分享圈API
    path('api/v1/shareloops/', ShareLoopListView.as_view(), name='shareloop-list'),
    # 分享圈上传API
    path('api/v1/shareloops/upload/', views.shareLoop_upload),
    # 用户API
    path('api/v1/users/', UserListView.as_view(), name='user-list'),
    # 心绪记录API
    path('api/v1/emotionrecords/', EmotionRecordListView.as_view(), name='emotionrecord-list'),
    # 食物地址API
    path('api/v1/foods/', FoodListView.as_view(), name='food-list'),
    # 管理员API
    path('admin/', admin.site.urls),
    # 测试地址
    path('api/test', views.api_test, name="api_test"),
]
