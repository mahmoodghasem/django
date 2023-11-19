from django.contrib import admin
from .models import *            #ایمپورت تمام مدلهای models.py در ادمین
from django_jalali.admin.filters import JDateFieldListFilter # ایمپورت تقویم شمسی
import django_jalali.admin as jadmin  # ایمپورت تقویم شمسی

admin.sites.AdminSite.site_header = "پروژه جنگو جهاد دانشگاهی" #صفحه ورود و عنوان اصلی ادمین
admin.sites.AdminSite.site_title = "پنل" # عنوان Tab
admin.sites.AdminSite.index_title = "" # زیر عنوان صفحه اصلی ادمین

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['position','title','status']
    list_filter = (['status'])
    search_fields = ['title','slug']
    prepopulated_fields = {'slug' : ['title']}

admin.site.register(Category, CategoryAdmin)


# ایمپورت مدل پستها @ برای دکوراتور بودنش هست
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    # نمایش ستونهای مطالب در ادمین
    list_display = ['title','author','publish','status', 'category_to_str']
    # مرتب سازی لیست مطالب در ادمین. میتونیم با تاپل هم بنویسیم ولی اگه تاپل یک گزینه داشت حتما بعدش کاما بذار
    ordering = ['title','publish']
    # فیلترهای کنار صفحه برای اینکه مثلا فقط نوشته های نویسنده مشخص را نمایش بده
    list_filter = ['author',('publish', JDateFieldListFilter),'status',('created', JDateFieldListFilter)]
    # جستجوی مطالب بر اساس موارد داخل لیست
    search_fields = ['title','description']
    # در صفحه ویرایش مطلب به کنار اسم نویسنده قابلیت جستجو برای تغییر آن اضافه میکند
    raw_id_fields = ['author']
    # فیلتر مطالب براساس تاریخ انتشار مطلب در بالای لیست مطالب
    date_hierarchy = 'publish'
    # نوشتن اتوماتیک slug براساس title
    prepopulated_fields = {'slug' : ['title']}
    # قابلیت ویرایش در لیست مطالب بدون باز کردن مطلب
    list_editable = ['status']
    # قابلیت کلیک برای باز کردن مطلب
    list_display_links = ['title']
    def category_to_str(self, obj):
        return '/'.join([category.title for category in obj.category.all()])



@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['name','subject','phone']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post','name','created','active']
    list_filter = ['active', ('created', JDateFieldListFilter), ('updated', JDateFieldListFilter)]
    search_fields = ['name', 'body']
    list_editable = ['active']



# خبرنامه
@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ['email']




