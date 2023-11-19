from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Comment


class TicketForm(forms.Form):
    SubjectChoises = (
        ('پشتیبانی فنی', 'پشتیبانی فنی'),
        ('سوالات پیش از خرید', 'سوالات پیش از خرید'),
        ('پیشنهادات و انتقادات', 'پیشنهادات و انتقادات'),
    )
    subject = forms.ChoiceField(choices=SubjectChoises, label='', widget=forms.Select(attrs={'dir': 'rtl', 'name': 'subject', 'class': 'form-control'}))
    name = forms.CharField(max_length=250, required=True, label='', widget=forms.TextInput(attrs = {'dir': 'rtl', 'name': 'name', 'type': 'text', 'class': 'form-control', 'placeholder': 'نام'}))
    phone = forms.CharField(max_length=11, required=True, label='', widget=forms.TextInput(attrs={'dir': 'rtl', 'name': 'phone', 'type': 'number', 'class': 'form-control', 'aria-describedby': 'emailHelp','placeholder': 'شماره تماس'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'dir': 'rtl', 'name': 'email', 'type': 'email', 'class': 'form-control', 'aria-describedby': 'emailHelp', 'placeholder': 'ایمیل'}))
    message = forms.CharField(required=True, label='', widget=forms.Textarea(attrs={'dir': 'rtl', 'name': 'message', 'type': 'text', 'class': 'form-control', 'placeholder': 'پیام خود را بنویسید'}))



# ثبت نام کاربر
class UserRegisterationForm(forms.Form):
    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'dir': 'rtl', 'name': 'firstname', 'class' : 'form-control form-control-lg', 'placeholder': 'نام'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'dir': 'rtl', 'name': 'lastname', 'class' : 'form-control form-control-lg', 'placeholder': 'نام نام خانوادگی'}))
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'dir': 'rtl', 'name': 'username', 'class' : 'form-control form-control-lg', 'placeholder': 'نام کاربری'}))
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'dir': 'rtl', 'name': 'email', 'class' : 'form-control form-control-lg', 'placeholder': 'ایمیل'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'dir': 'rtl', 'name': 'password', 'class': 'form-control form-control-lg', 'placeholder': 'رمز عبور'}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'dir': 'rtl', 'name': 'confirm_password', 'class': 'form-control form-control-lg', 'placeholder': 'تأیید رمز عبور'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("رمز عبور و تأیید آن یکسان نیستند.")

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("ایمیل قبلاً ثبت شده است. لطفاً از ایمیل دیگری استفاده کنید.")
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("نام کاربری قبلاً ثبت شده است. لطفاً از نام کاربری دیگری استفاده کنید.")
        return username



# لاگین کاربر
class UserLoginForm(forms.Form):
    username = forms.CharField(label='', widget=forms.TextInput(attrs={'dir': 'rtl', 'name': 'username', 'class' : 'form-control form-control-lg', 'placeholder': 'نام کاربری'}))
    password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'dir': 'rtl', 'name': 'password', 'class' : 'form-control form-control-lg', 'placeholder': 'رمز عبور'}))

# فرم کامنت
class CommentForm(forms.ModelForm):
    def clean_name(self):
        name = self.cleaned_data['name']
        if name:
            if len(name) < 4:
                raise forms.ValidationError("لطفا نام صحیح خود را وارد کنید!")
            else:
                return name
    class Meta:
        model = Comment
        fields = ['name', 'body']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'نام خود را وارد کنید'}),
            'body': forms.Textarea(attrs={'class': 'form-control comment', 'placeholder': 'نظر خود را اینجا بنویسید...'}),
        }
        labels = {
            'name': '',
            'body': '',
            # برای هر فیلدی که می‌خواهید برچسب حذف شود، یک label خالی مشخص کنید.
        }



# اشتراک در خبرنامه
class SubscriptionForm(forms.Form):
    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'dir': 'rtl', 'name': 'email', 'type': 'email', 'class': 'form-control', 'aria-describedby': 'emailHelp', 'placeholder': 'ایمیل خود را وارد کنید'}))












