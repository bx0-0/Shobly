import os
from django.db import models
import uuid
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


def GetImageUploadTo(instance, ImageName):
    name, ext = os.path.splitext(ImageName)
    id = uuid.uuid4()
    return f"product_imgs/{id}{ext}"


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return str(_(self.name))


class Product(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255, verbose_name="Product Name")

    amount = models.PositiveIntegerField()

    description = models.TextField(max_length=1000, verbose_name="Product Description")

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(1.0)],
        verbose_name="Price (EGP)",
    )

    summary = models.TextField(
        max_length=150,
        help_text="summary of product description",
        verbose_name="Summary",
    )

    catigory = models.ForeignKey("Category", on_delete=models.CASCADE)

    product_color = models.CharField(max_length=100, verbose_name="Product Color")

    img1 = models.ImageField(
        upload_to=GetImageUploadTo, verbose_name="upload first image for product"
    )

    img2 = models.ImageField(
        upload_to=GetImageUploadTo, verbose_name="upload second image for product"
    )

    slug = models.SlugField(unique=True, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(uuid.uuid4())
        super(Product, self).save(*args, **kwargs)


class Rating(models.Model):

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="ratings"
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    created_at = models.DateTimeField(auto_now_add=True)
