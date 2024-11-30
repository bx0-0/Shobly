import os
from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

# دي الفانكشن اللي بتحدد مسار تحميل الصورة
# بتاخد `instance` اللي هو بروفايل المستخدم و `ImageName` اسم الصورة.
# بتنشئ ID فريد لكل صورة جديدة باستخدام `uuid4` عشان الصور متبقاش متكررة.
def GetImageUploadTo(instance, ImageName):
    name, ext = os.path.splitext(ImageName)  # هنا بنفصل الاسم عن الامتداد
    id = uuid.uuid4()  # بنعمل ID فريد للصورة
    return f"product_imgs/{id}{ext}"  # بنرجع المسار اللي الصورة هتتحمل فيه


# هنا بنعرف موديل الفئة (Category) اللي هيتعمل لها تصنيف للمنتجات
class Category(models.Model):
    # ده الحقل اللي هيحمل اسم الفئة
    name = models.CharField(max_length=100, unique=True)
    # ده الوصف بتاع الفئة لو حابب تكتب عنها أكتر
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name  # هيعرض اسم الفئة لما نطبع الكائن ده


# موديل المنتج اللي هيتخزن فيه كل التفاصيل بتاعة المنتج
class Product(models.Model):
    # المستخدم اللى عامل المنتج ده (اللي هو اليوزر)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # اسم المنتج
    title = models.CharField(max_length=255, verbose_name="Product Name")
    # الكمية المتاحة من المنتج
    amount = models.PositiveIntegerField()
    # الوصف بتاع المنتج
    description = models.TextField(max_length=1000, verbose_name="Product Description")
    # السعر بتاع المنتج
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1.0)],  verbose_name="Price (EGP)")
    # ملخص عن المنتج (اللي هيظهر في تفاصيل المنتج بشكل مختصر)
    summary = models.TextField(max_length=150, help_text='summary of product description', verbose_name="Summary")
    # الفئة اللي بينتمي ليها المنتج (دورة الربط مع الـCategory)
    catigory = models.ForeignKey('Category', on_delete=models.CASCADE)
    # اللون بتاع المنتج
    product_color = models.CharField(max_length=100, verbose_name="Product Color")
    # الصور بتاع المنتج (اول صورة)
    img1 = models.ImageField(upload_to=GetImageUploadTo, verbose_name="upload first image for product")
    # الصورة التانية للمنتج
    img2 = models.ImageField(upload_to=GetImageUploadTo, verbose_name="upload second image for product")
    # هنا الـslug ده اللى هيكون رابط الـURL الفريد لكل منتج
    slug = models.SlugField(unique=True, null=True, blank=True)
    # تاريخ انشاء المنتج
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title  # عند طباعة المنتج هيعرض اسمه فقط


# موديل التقييمات اللي هيتخزن فيها التقييمات الخاصة بكل منتج
class Rating(models.Model):
    # الربط مع المنتج
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="ratings")
    # اليوزر اللى عمل التقييم
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # التقييم اللي هيتعطى للمنتج (من 1 ل 5)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])  # التقييم بعدد النجوم من 1 إلى 5
    # تاريخ التقييم
    created_at = models.DateTimeField(auto_now_add=True)
