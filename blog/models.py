from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User # برای مدیریت یوزرها
from django_jalali.db import models as jmodels # تاریخ شمسی
from django.urls import reverse
from ckeditor.fields import RichTextField
from datetime import date


#  manager اختصاصی برای مدل پست
class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)

# دسته‌بندی
class Category(models.Model):
    title = models.CharField(max_length=250, verbose_name='عنوان دسته‌بندی')
    slug = models.SlugField(max_length=250, verbose_name='آدرس دسته‌بندی')
    status = models.BooleanField(default=True, verbose_name = 'فعال | غیرفعال')
    position = models.IntegerField(verbose_name='موقعیت')
    class Meta:
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
        ordering = ['position']

    def __str__(self):
        return self.title


# پست‌ها
class Post(models.Model):
   #  ForeignKey: برای ایجاد رابطه چند به یک
   #  User جدولی هست که میخوایم بهش وصل شه
   #  on_delete برای وقتیه که یوزر حذف شد چه بلایی سر پستهاش بیاد
   #  None: پستها حذف نمیشه models.CASCADE: پستهاش حذف میشه
   # برای دسترسی از طریق اون یکی جدول (User) related_name = user_posts
   # default مقدار پیشفرض
   # verbose_name برای عنوان ستونهای صفحه ادمین است
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_posts', default=1, verbose_name = 'نویسنده')
    # عنوان مطلب
    title = models.CharField(max_length=250, verbose_name = 'عنوان')
    category = models.ManyToManyField(Category, verbose_name='دسته‌بندی')
   # تصویر
    photo = models.ImageField(upload_to='images')
    # توضیحات
    description = models.TextField(verbose_name = 'توضیحات')
   # محتوا
    content = RichTextField(verbose_name='محتوا')
    # url پست
    slug = models.SlugField(max_length=250, verbose_name = 'پیوند')
    # زمان فعلی انتشار پست
    publish = jmodels.jDateTimeField(default=timezone.now, verbose_name = 'زمان انتشار مطلب')
    # زمان ایجاد پست
    created = jmodels.jDateTimeField(auto_now_add = True, verbose_name = 'زمان ایجاد مطلب')
    # زمان آپدیت پست
    update = jmodels.jDateTimeField(auto_now_add=True, verbose_name = 'زمان بروزرسانی مطلب')
    # تعداد بازدید پست
    views_count = models.IntegerField(default=0)
    # کلاس وضعیت پست مثل radio button میمونه
    class Status(models.TextChoices):
        DRAFT = 'DF', 'در صف بررسی'
        PUBLISHED = 'PB', 'منتشر شده'
        REJECTED = 'RJ', 'رد شده'
    # فیلد وضعیت پست
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT, verbose_name = 'وضعیت انتشار')
    # objects = models.Manager()
    objects = jmodels.jManager() # برای تغییر به تاریخ شمسی در منیجر اختصاصی
    published = PublishedManager() # نگه داشتن منیجر پیشفرض خودش

    class Meta:
        # مرتب سازی پست ها (منفی برای معکوس کردنش هست(جدیدترینها) برای ادمین پنل
        ordering = ['-publish']
        #  ایندکس براساس تاریخ انتشار برای دیتا بیس
        indexes = [
            models.Index(fields=['-publish'])
        ]
        verbose_name = 'پست' # عنوان مفرد بخش پست در ادمین
        verbose_name_plural = 'پست‌ها' # عنوان جمع بخش پست ها در ادمین

    def __str__(self):
        #  نمایش عنوان هر مطلب در لیست مطالب منتشر شده در صفحه ادمین
        return self.title
    # متد ایجاد url (با این متد یک دکمه در ادمین پنل ایجاد می شود به نام مشاهده در وبگاه) reverse نیاز به ایمپورت دارد
    def get_absolute_url(self):
        # reverse کارش اینه که url را با توجه به آرگومانی که بهش میدیم صدا میزنه
        #  accounts:post_detail همون url ما هست (namespase=accounts , name=post_detail) یعنی همون '/<posts/<int:id' داخل url اپ
        return reverse('blog:post_detail', args=[self.id])





class Ticket(models.Model):
    message = models.TextField(verbose_name = 'پیام')
    name = models.CharField(max_length=250, verbose_name = 'نام')
    email = models.EmailField(verbose_name = 'ایمیل')
    phone = models.CharField(max_length=11, verbose_name = 'شماره تماس')
    subject = models.CharField(max_length=250, verbose_name = 'موضوع')
    class Meta:
        verbose_name = 'تیکت' # عنوان مفرد بخش تیکت در ادمین
        verbose_name_plural = 'تیکت‌ها' # عنوان جمع بخش تیکت ها در ادمین
    def __str__(self):
        #  نمایش موضوع تیکت لیست تیکت‌ها در صفحه ادمین
        return self.subject

# کامنت‌گذاری
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', default=1, verbose_name = 'مطلب')
    name = models.CharField(max_length=250, verbose_name = 'نام')
    body = models.TextField(verbose_name='کامنت')
    created = jmodels.jDateTimeField(auto_now_add = True, verbose_name = 'زمان ایجاد کامنت')
    updated = jmodels.jDateTimeField(auto_now=True, verbose_name = 'زمان بروزرسانی کامنت')
    active = models.BooleanField(default=False, verbose_name='تایید کامنت')
    class Meta:
        ordering = ['-created']
        indexes = [
            models.Index(fields=['-created'])
        ]
        verbose_name = 'نظر'
        verbose_name_plural = 'نظرات'

    def __str__(self):
        return f"{self.name} : {self.post}"



# خبرنامه
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.email
    class Meta:
        verbose_name = 'ایمیل'
        verbose_name_plural = 'خبرنامه'

#مدل مرتبط با وضعیت کارمندی
class EmployeeStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee_status')
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Employee Status"

