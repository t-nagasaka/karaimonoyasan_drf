from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator


# upload_toのパス作成関数
def upload_avatar_path(instance, filename):
    # 拡張子を取り出し(例：jpgやpng)
    ext = filename.split('.')[-1]
    # 保存先のパスを作成して返却
    return '/'.join([
        'avatars',
        str(instance.userProfile.id)+str(instance.nickName)+str('.')+str(ext)])


# upload_toのパス作成関数
def upload_post_path(instance, filename):
    # 拡張子を取り出し(例：jpgやpng)
    ext = filename.split('.')[-1]
    # 保存先のパスを作成して返却
    return '/'.join([
        'posts',
        str(instance.userPost.id)+str(instance.title)+str('.')+str(ext)])


# 管理者ユーザーモデル作成(email対応のオーバーライド)
class UserManager(BaseUserManager):
    # 通常usernameとpasswordでユーザーを作成するが、
    # 今回はemailとpasswordの設定に変更
    def create_user(self, email, password=None):
        # emailがない場合の例外処理
        if not email:
            raise ValueError('email is must')
        # emailの正規化(例：小文字変更など)
        user = self.model(email=self.normalize_email(email))
        # パスワードのハッシュ化
        user.set_password(password)
        # 作成したユーザーをDBに保存
        user.save(using=self._db)
        return user

    # ユーザーマネージャをカスタムした場合はsuperuserも設定する必要がある
    # usernameからemailへ変更
    def create_superuser(self, email, password):
        user = self.create_user(email, password)
        # AdminのDashboardにログインする権限
        user.is_staff = True
        # AdminのDashboardにログイン+内容の変更権限
        user.is_superuser = True
        # 作成したユーザーをDBに保存
        user.save(using=self._db)
        return user


# 一般ユーザーモデル作成(email対応のオーバーライド)
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # UserManagerをネストする
    objects = UserManager()

    # デフォルトのusernameをemailへオーバーライド
    USERNAME_FIELD = 'email'

    # emailの文字列を返却
    def __str__(self):
        return self.email


# プロフィールモデル作成
class Profile(models.Model):
    nickName = models.CharField(max_length=20)
    # 辛いもの耐性
    spicy_resist = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)])
    # 関連する対象のモデルを指定, 呼び名の指定, 対象の削除時の挙動
    userProfile = models.OneToOneField(settings.AUTH_USER_MODEL,
                                       related_name='userProfile',
                                       on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    # upload_toで保存するパスを指定
    img = models.ImageField(blank=True, null=True, upload_to=upload_avatar_path)

    def __str__(self):
        return self.nickName


# ポストモデル作成
class Post(models.Model):
    title = models.CharField(max_length=200)
    # (ForeignKey == OnToMany)　
    # 関連する対象のモデルを指定, 呼び名の指定, 対象の削除時の挙動
    spicy_level = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0),
                    MaxValueValidator(10)])
    userPost = models.ForeignKey(settings.AUTH_USER_MODEL,
                                 related_name='userPost',
                                 on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    # upload_toで保存するパスを指定
    img = models.ImageField(blank=True, null=True, upload_to=upload_post_path)
    # 関連する対象のモデルを指定, 呼び名の指定
    liked = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='liked',
                                   blank=True)

    def __str__(self):
        return self.title


# コメントモデル作成
class Comment(models.Model):
    text = models.CharField(max_length=255)
    # 関連する対象のモデルを指定, 呼び名の指定, 対象の削除時の挙動
    userComment = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    related_name='userComment',
                                    on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # 辛さ


    class Meta:
        db_table = 'comments'
        verbose_name_plural = 'コメント'


# リプライモデル作成
class Replay(models.Model):
    replay = models.CharField(max_length=255)
    # 関連する対象のモデルを指定, 呼び名の指定, 対象の削除時の挙動
    commentReplay = models.OneToOneField(Comment,
                                         related_name='commentReplay',
                                         on_delete=models.CASCADE)

    class Meta:
        db_table = 'replays'
        verbose_name_plural = 'リプライ'
