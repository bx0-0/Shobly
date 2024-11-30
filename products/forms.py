from django import forms
from .models import Product

# هنا بنعرف الفورم الخاص بالمنتج اللي هيتعمل بيه إضافة أو تعديل للمنتج
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product  # بنحدد إن الفورم ده مربوط بموديل الـProduct
        fields = ['title', 'description', 'price', 'summary', 'catigory', 'img1', 'img2']  # الحقول اللي هنعرضها في الفورم

        # هنا بنحدد شكل الـwidgets الخاص بكل حقل
        widgets = {
            # الـ'catigory' هو الحقل الخاص باختيار الفئة (الفئة اللي ينتمي ليها المنتج)
            'catigory': forms.Select(attrs={
                'class': 'form-control',  # بنضيف كلاس CSS عشان الشكل يبقى مرتب
                'style': 'width: 100%; font-size: 18px;'  # بنضيف ستايل لتحديد العرض وحجم الخط
            }),
            # الـ'img1' هو الحقل الخاص برفع أول صورة للمنتج
            'img1': forms.FileInput(attrs={
                'class': 'form-control',  # نفس الكلاس اللي استخدمناه في الفئة
                'style': 'width: 100%; font-size: 18px;'  # نفس الاستايل
            }),
            # الـ'img2' هو الحقل الخاص برفع الصورة التانية للمنتج
            'img2': forms.FileInput(attrs={
                'class': 'form-control',  # كمان هنا بنضيف نفس الكلاس
                'style': 'width: 100%; font-size: 18px;'  # استايل متناسق مع باقي الحقول
            }),
        }
