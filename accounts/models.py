import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from cities_light.models import City # type: ignore

# دي الفانكشن اللي بتحدد مسار تحميل الصورة
# بتاخد `instance` اللي هو بروفايل المستخدم و`ImageName` اسم الصورة.
# بتنشئ ID فريد لكل صورة جديدة باستخدام `uuid4` عشان الصور متبقى متكررة.
def GetImageUploadTo(instance, ImageName):
    name, ext = os.path.splitext(ImageName)  # هنا بنفصل الاسم عن الامتداد
    id = uuid4()  # بنعمل ID فريد للصورة
    return f"profile/{id}{ext}"  # بنرجع المسار اللي الصورة هتتحمل فيه

class Profile(models.Model):
    # ربط البروفايل بالمستخدم باستخدام `ForeignKey` عشان كل مستخدم يبقى عنده بروفايل واحد
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile', db_index=True)

    # ربط المدينة بالبروفايل، لو تمسحت المدينة بيخليها Null بدل ما يمسح البروفايل
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True, related_name='profile_city')

    # بيانات اضافية للبروفايل، زي الوصف واسم الشركة
    about = models.TextField(null=True, blank=True, help_text='About User  will appear in  all products that published')
    company_name = models.CharField(max_length=255, null=True, blank=True, help_text='Company  Name will appear in  all  products you published')

    # صورة البروفايل مع مسار تحميل مخصص
    ProfileImg = models.ImageField(upload_to=GetImageUploadTo, null=True, blank=True)

    # عرض اسم المستخدم في الأدمن بدل ما يظهر ID البروفايل
    def __str__(self) -> str:
        return self.user.username

    # الفانكشن دي بتحفظ البروفايل وتتعامل مع تعديل الصورة
    # لو البروفايل كان فيه صورة قديمة وبنغيرها، بتحذف الصورة القديمة عشان مساحة التخزين.
    def save(self, *args, **kwargs):
        if self.pk and self.ProfileImg:  # تأكد أن البروفايل موجود وصورة جديدة موجودة
            try:
                old_img = Profile.objects.get(pk=self.pk).ProfileImg  # تجيب الصورة القديمة
            except Profile.DoesNotExist:
                old_img = None

            # لو فيه صورة قديمة والصورة الجديدة غيرها، بتحذف القديمة من الجهاز
            if old_img and old_img != self.ProfileImg:
                if os.path.isfile(old_img.path):  # تتأكد إن الصورة فعلاً موجودة في الجهاز
                    os.remove(old_img.path)  # تحذف الصورة القديمة

        return super().save(*args, **kwargs)  # تكمل حفظ البروفايل
