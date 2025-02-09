import os
from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User
from cities_light.models import City


def GetImageUploadTo(instance, ImageName):
    name, ext = os.path.splitext(ImageName)
    id = uuid4()
    return f"profile/{id}{ext}"


class Profile(models.Model):

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="profile", db_index=True
    )

    city = models.ForeignKey(
        City,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile_city",
    )

    about = models.TextField(
        null=True,
        blank=True,
        help_text="About User  will appear in  all products that published",
    )
    company_name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Company  Name will appear in  all  products you published",
    )

    paypal_email = models.EmailField(
        null=True,
        blank=True,
        help_text="Paypel Email not appear in  public profile only for  payment process if you sell product",
    )

    ProfileImg = models.ImageField(upload_to=GetImageUploadTo, null=True, blank=True)

    def __str__(self) -> str:
        return self.user.username

    def save(self, *args, **kwargs):
        if self.pk and self.ProfileImg:
            try:
                old_img = Profile.objects.get(pk=self.pk).ProfileImg
            except Profile.DoesNotExist:
                old_img = None

            if old_img and old_img != self.ProfileImg:
                if os.path.isfile(old_img.path):
                    os.remove(old_img.path)

        return super().save(*args, **kwargs)
