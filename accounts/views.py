from typing import Any
from django.db.models.base import Model as Model
from django.forms import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from .models import Profile
from .forms import ProfileForm, SingUpForm, UserForm
from django.views.generic import TemplateView
from django.db import transaction


class SignUpView(CreateView):
    form_class = SingUpForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    
    # الدالة دي بتشتغل لما حد يضغط على زرار "تسجيل" عشان يسجل حساب جديد.
    #  الـ `transaction.atomic` هنا بتأكد إن كل حاجة بتتحفظ في الداتا بيز صح
    # لو في خطوات كتير أو بيانات جاية من كذا مكان.
    @transaction.atomic
    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return super().post(request, *args, **kwargs)
    
    # الدالة دي بتشتغل لما البيانات اللي اتكتبت في الفورم صح.
    # هنا بنعمل بروفايل جديد للمستخدم اللي لسه سجل ونحفظ فيه "المدينة" اللي دخلها.
    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        response = super().form_valid(form)
        if self.object:  # "self.object" هو المستخدم الجديد اللي سجل
           profile = Profile.objects.create(user=self.object)
           profile.city = form.cleaned_data.get('city')  # حفظ المدينة في البروفايل
           profile.save()  # حفظ البروفايل في الداتا بيز
           
        return response

class ShowProfileView(TemplateView):
    template_name = "registration/profile.html"
    
    # الدالة دي بتجهز البيانات اللي هتتعرض في صفحة البروفايل.
    # هنا بنجيب البروفايل الخاص بالمستخدم اللي سجل دخول ونعرضه في الصفحة.
    def get_context_data(self, **kwargs:Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)  # بنجيب البروفايل للمستخدم الحالي
        context["profile"] = profile  # نضيف البروفايل للـ context عشان نقدر نعرضه في القالب
        return context
    

class ProfileUpdateView(UpdateView):
    template_name = "registration/edit_profile.html"
    form_class = ProfileForm
    success_url = '../profile/'
    
    # الدالة دي بتجيب البروفايل اللي هنعدله، وبتتأكد إنه بتاع المستخدم الحالي.
    def get_object(self, queryset=None):
        obj = Profile.objects.get(user=self.request.user)  # نجيب البروفايل للمستخدم اللي سجل دخول
        return obj

    # الدالة دي بتجهز البيانات اللي هتظهر في فورم تعديل البروفايل.
    # هنا بنضيف فورم تاني للبيانات العامة للمستخدم زي الاسم والبريد الإلكتروني جنب بيانات البروفايل.
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserForm(instance=self.request.user)  # فورم المستخدم للتفاصيل الأساسية
        return context

    # الدالة دي بتشتغل لما الفورم اتملأ بشكل صحيح.
    # هنا بنراجع على الفورم التاني بتاع بيانات المستخدم العامة، ولو صح بنحفظه.
    def form_valid(self, form):
        user_form = UserForm(self.request.POST, instance=self.request.user)  # فورم البيانات العامة
        if user_form.is_valid():
            user_form.save()  # نحفظ بيانات المستخدم العامة
        return super().form_valid(form)  # نحفظ التعديلات على البروفايل ونكمل التحديث
