from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from cities_light.models import City   # type: ignore

# ده الفورم الخاص بالتسجيل، بيستخدمه المستخدمين الجدد عشان يسجلوا حساب
class SingUpForm(UserCreationForm):
    # هنا بنحدد حقل المدينة، وعملناها HiddenInput عشان ما تظهرش
    city = forms.ModelChoiceField(City.objects.all(), widget=forms.HiddenInput())
    # البريد الإلكتروني مش مطلوب
    email = forms.EmailField(required=False, help_text='Emial not requiered')
    
    class Meta:
        model = User  # الموديل اللي هيتم استخدامه عشان نحفظ البيانات
        fields = ('username', 'email', 'city', 'password1', 'password2')  # الحقول اللي هيظهروا في الفورم

# ده الفورم الخاص بتحديث بيانات المستخدم
class UserForm(forms.ModelForm):
    class Meta:
        model = User  # هنا بنحدث بيانات الموديل User
        fields = ['username', 'email']  # الحقول اللي عايزين نسمح بتعديلها

# ده الفورم الخاص بتحديث البروفايل
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile  # هنا بنحدث البيانات الخاصة بالبروفايل
        fields = ['about', 'company_name', 'city', 'ProfileImg']  # الحقول الخاصة بالبروفايل
