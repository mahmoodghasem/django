from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView, PasswordResetView



app_name = 'blog'


urlpatterns = [
    # قبل تمام این urlها، url اصلی میاد که مال اپ هست: .../blog/...
    path('',views.PostList.as_view(), name='post_list'), # مسیر کلاس بیس ویو
    # path('posts/<int:id>/',views.post_detail, name='post_detail'),
    path('posts/<pk>/', views.post_detail, name='post_detail'),  # جزییات پست
    path('posts/<post_id>/comment/',views.post_comment, name='post_comment'), # نظرات
    path('ticket/',views.ticket, name='ticket'), # مسیر فرم تیکت
    path('register/', views.user_register,name='user_register'), # ثبت نام کاربر
    path('login/', views.user_login, name='login'), # لاگین کاربر
    path('logout/',views.user_logout, name='logout'), # خروج کاربر
    path('search/', views.search, name='search'), # جستجو
    path('passwordchange/', PasswordChangeView.as_view(template_name='forms/passwordchange.html'), name='passwordchange'), # تغییر پسورد
    path('subscribe/', views.subscribe, name='subscribe'), # خبرنامه
]







