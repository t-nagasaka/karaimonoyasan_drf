from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


# アップネームを指定(必須)
app_name = 'user'

# routerのインスタンス化(必須)
router = DefaultRouter()
# ModelViewSetを継承したViewのみrouterでルーティングができる
router.register('profile', views.ProfileViewSet)
router.register('post', views.PostViewSet)
router.register('comment', views.CommentViewSet)
router.register('replay', views.ReplayViewSet)

# genericで作成した汎用Viewは通常のurlpatternsで定義する
urlpatterns = [
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('myprofile/', views.MyProfileListView.as_view(), name='myprofile'),
    # routerも指定する(必須)
    path('', include(router.urls))
]
