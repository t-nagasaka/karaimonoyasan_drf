from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # apiAppsのルートを指定
    path('api/', include('api.urls')),
    # authen/jwt/create/でJWTのトークンを発行する
    path('authen/', include('djoser.urls.jwt')),
]

# settings.pyに追加したMEDIA_URLとMEDIA_ROOTから画像へのルートを指定
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
