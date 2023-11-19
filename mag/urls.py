from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    # این url صفحه اصلی هر اپ هست و باید قبل از تمام urlهای اپ بیاد
    path('', include('blog.urls', namespace="blog")),
]
# افزودن پترن برای فایل‌های رسانه
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

