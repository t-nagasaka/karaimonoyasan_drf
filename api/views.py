from rest_framework import generics, viewsets
from rest_framework.permissions import AllowAny
from . import serializers
from .models import Profile, Post, Comment, Replay


# ModelViewSet
# すべてのCRUD処理が可能
# 個別で指定したいときは対象CRUDのAPIViewを指定

# 新規ユーザー作成処理の作成
# 作成のみのためCreateAPIViewを使用
class CreateUserView(generics.CreateAPIView):
    # 対象のserializerを指定(必須)
    serializer_class = serializers.UserSerializer
    # JWTの認証を誰でも可に上書き
    permission_classes = (AllowAny,)


# プロフィール作成、変更処理の作成
# 作成、照会、変更などがあるため、viewsets.ModelViewSetを使用
class ProfileViewSet(viewsets.ModelViewSet):
    # すべてのプロフィールを取得
    queryset = Profile.objects.all()
    # 対象のserializerを指定(必須)
    serializer_class = serializers.ProfileSerializer

    # オーバーライドメソッド
    def perform_create(self, serializer):
        # ログインしているユーザーの情報を取得して保存
        serializer.save(userProfile=self.request.user)


# ログインしているユーザーの情報を返す
class MyProfileListView(generics.ListAPIView):
    # すべてのプロフィールを取得
    queryset = Profile.objects.all()
    # 対象のserializerを指定(必須)
    serializer_class = serializers.ProfileSerializer

    # オーバーライドメソッド
    def get_queryset(self):
        # ログインしているユーザーの情報を取得して返却
        return self.queryset.filter(userProfile=self.request.user)


# 投稿の作成、変更処理の作成
class PostViewSet(viewsets.ModelViewSet):
    # すべての投稿を取得
    queryset = Post.objects.all()
    # 対象のserializerを指定(必須)
    serializer_class = serializers.PostSerializer

    # オーバーライドメソッド
    def perform_create(self, serializer):
        # ログインしているユーザーの情報を取得して保存
        serializer.save(userPost=self.request.user)


# コメントの作成、変更処理の作成
class CommentViewSet(viewsets.ModelViewSet):
    # すべてのコメントを取得
    queryset = Comment.objects.all()
    # 対象のserializerを指定(必須)
    serializer_class = serializers.CommentSerializer

    # オーバーライドメソッド
    def perform_create(self, serializer):
        # ログインしているユーザーの情報を取得して保存
        serializer.save(userComment=self.request.user)


# コメントの作成、変更処理の作成
class ReplayViewSet(viewsets.ModelViewSet):
    # すべてのコメントを取得
    queryset = Replay.objects.all()
    # 対象のserializerを指定(必須)
    serializer_class = serializers.ReplaySerializer

    # オーバーライドメソッド
    def perform_create(self, serializer):
        # ログインしているユーザーの情報を取得して保存
        serializer.save(commentReplay=self.request.user)
