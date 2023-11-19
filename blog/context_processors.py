from .models import Post

# جدیدترین مطالب
def recent_posts(request):
    recent_posts = Post.objects.order_by('-publish')[:5]
    return {'recent_posts' : recent_posts}

# مرتب‌سازی مطالب بر اساس تعداد بازدیدها به صورت نزولی
def most_viewed_articles(request):
    most_viewed = Post.objects.all().order_by('-views_count')[:5]  # 5 پست با بیشترین بازدید
    return {'most_viewed_articles': most_viewed}
