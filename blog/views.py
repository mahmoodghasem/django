from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView
from .models import *
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.views.generic import DetailView
from .models import Post


def blog_home(request):
    return render(request, 'blog/blog.html')

# def post_list(request):
#     posts = Post.objects.filter(status='PB')
#     #   شماره صفحات (صفحه‌بندی) posts المانهای صفحه‌بندی ماست و عدد بعدش یعنی ۳ تعداد پستها در هر صفحه است
#     paginator = Paginator(posts, 3)
#     # page شماره صفحه است و عدد بعدش مقداری هست که درصورت پیدا نکردن page برمیگردونه
#     page_number = request.GET.get('page',1)
#     try:
#         posts = paginator.page(page_number)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     context = {
#         # مقدار سمت راست دیکشنری همون متغییر بالاست
#         'posts': posts,
#     }
#     return render(request , 'accounts/list.html' , context)

class PostList(ListView):
    # نمایش تمام پستهای منتشر شده
    queryset = Post.published.all()
    # اسم تغییر دلخواه برای استفاده در html
    context_object_name = 'posts'
    # تعداد آیتمهای موجود در هر صفحه
    paginate_by = 3
    # اگر اسمش را میذاشتیم list.html دیگه نیازی نبود خط پایینم بنویسیم خودش میفهمید
    template_name = 'blog/list.html'


def post_detail(request, pk):
    post = get_object_or_404(Post, id=pk, status=Post.Status.PUBLISHED)
    comments = post.comments.filter(active=True)
    form = CommentForm()
    context = {
        'post' : post,
        'form' : form,
        'comments' : comments,
        'category' : Category.objects.filter(status=True),
        'new_date' : datetime.now(), # برای تست کردن تاریخ در html
    }
    return render(request, 'blog/detail.html' , context)



# class PostDetail(DetailView):
#     model = Post
#     template_name = 'blog/detail.html'
#     context_object_name = 'post'



def ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            # به save نیاز نیست چون create خودش ذخیره هم میکنه
            cd = form.cleaned_data
            Ticket.objects.create(message = cd['message'],name = cd['name'],email = cd['email'],phone = cd['phone'],subject = cd['subject'])
            # یا کد زیر به همراه save:
            # ticket_obj = Ticket.objects.create()
            # cd = form.cleaned_data
            # ticket_obj.message = cd['message']
            # ticket_obj.name = cd['name']
            # ticket_obj.email = cd['email']
            # ticket_obj.phone = cd['phone']
            # ticket_obj.subject = cd['subject']
            # ticket_obj.save()
            # پیغام ارسال موفق پیام
            messages.success(request, 'پیام شما با موفقیت ارسال شد.')
            return redirect('blog:ticket')

    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form' : form})

# ثبت نام کاربر
def user_register(request):
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            # ایجاد رکورد مرتبط با وضعیت کارمندی
            employee_status = EmployeeStatus(user=user, is_active=True)  # در اینجا فرض کرده‌ام که یک فیلد به نام 'is_active' برای وضعیت فعالیت کارمندی وجود دارد
            employee_status.save()
            messages.success(request, 'شما با موفقیت ثبت نام شدید.')
            return redirect('blog:user_register')
    else:
        form = UserRegisterationForm()
    return render(request, 'forms/register.html', {'form': form})

# ورود کاربر
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.info(request, 'شما با موفقیت وارد سایت شدید.')
                return redirect('blog:post_list')
            else:
                messages.error(request, 'نام کاربری یا رمز عبور اشتباه است!')
    else:
        form = UserLoginForm()
    return render(request, 'forms/login.html', {'form' : form})

# خروج کاربر
@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, 'شما با موفقیت خارج شدید.')
    return redirect(reverse('blog:post_list'))

# نظرات
@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.save()
        messages.success(request, 'نظر شما با موفقیت ارسال شد و پس از تایید منتشر خواهد شد.♥️')
    else:
        messages.error(request, 'لطفاً اطلاعات معتبر وارد کنید.')
    return redirect('blog:post_detail', pk=post_id)


# جستجو
def search(request):
    if request.method == 'POST':
        query = request.POST.get('search_input')
        if query:
            # جستجو در عنوان و محتوا
            results = Post.published.filter(Q(title__icontains=query) | Q(content__icontains=query))
            posts = results

            if not results:
                messages.error(request, 'متاسفانه نتیجه ای یافت نشد!', extra_tags='text-danger')

            return render(request, 'blog/list.html', {'posts': posts, 'query': query})

    return render(request, 'blog/list.html', {'posts': None, 'query': None})



# اشتراک در خبرنامه
def subscribe(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # بررسی وجود ایمیل در دیتابیس
            subscriber, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.info(request, 'ایمیل شما با موفقیت ثبت شد.')
            else:
                messages.error(request, 'ایمیل شما قبلاً ثبت شده است.')
    else:
        form = SubscriptionForm()
    return render(request, 'include/subscribe.html', {'form': form})


# دسته‌بندی‌ها
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})



