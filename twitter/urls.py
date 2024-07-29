from django.urls import path,include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('tweets/',include('tweets.urls')),
    path('user/', include('follow.urls')),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path('tweets/',include('liketweet.urls')),
    path('tweets/',include('commenttweet.urls')),
    path('user/',include('notification.urls'))
]   

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

