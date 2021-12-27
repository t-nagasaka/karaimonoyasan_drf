from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile, Post, Comment, Replay


# ユーザーのシリアライザー設定
class UserSerializer(serializers.ModelSerializer):
    # メタ情報の設定
    class Meta:
        # 対象となるモデルの指定
        model = get_user_model()
        # 使用するフィールドの設定
        fields = ('id', 'email', 'password')
        # 追加設定(write_onlyではgetでユーザー情報にアクセスしてもレスポンスは返ってこない)
        extra_kwargs = {'password': {'write_only': True}}

    # 新規作成時の設定(オーバーライド)
    # validated_dataにはemailとpasswordが格納される(validation OKの場合)
    def create(self, validated_data):
        # models.pyで定義したUser→UserManager→create_userメソッドの実行
        user = get_user_model().objects.create_user(**validated_data)
        return user


# プロフィールのシリアライザー設定
class ProfileSerializer(serializers.ModelSerializer):
    # Djangoの表記が細かいため。年月日に指定
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Profile
        fields = (
            'id', 'nickName', 'userProfile', 'spicy_resist',
            'created_on', 'img')
        extra_kwargs = {'userProfile': {'read_only': True}}


# ポスト(投稿)のシリアライザー設定
class PostSerializer(serializers.ModelSerializer):
    # Djangoの表記が細かいため。年月日に指定
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Post
        fields = (
            'id', 'title', 'userPost', 'spicy_level',
            'created_on', 'img', 'liked')
        extra_kwargs = {'userPost': {'read_only': True}}


# コメントのシリアライザー設定
class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'userComment', 'post')
        extra_kwargs = {'userComment': {'read_only': True}}


# リプライ(返信)のシリアライザー設定
class ReplaySerializer(serializers.ModelSerializer):
    # Djangoの表記が細かいため。年月日に指定
    created_on = serializers.DateTimeField(format='%Y-%m-%d', read_only=True)

    class Meta:
        model = Replay
        fields = ('id', 'replay', 'commentReplay')
        extra_kwargs = {'commentReplay': {'read_only': True}}
