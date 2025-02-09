from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Product


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "title",
            "description",
            "price",
            "amount",
            "summary",
            "catigory",
            "img1",
            "img2",
        ]

        labels = {
            "title": _("Product Title"),
            "description": _("Description"),
            "price": _("Price"),
            "amount": _("Amount"),
            "summary": _("Summary"),
            "catigory": _("Category"),
            "img1": _("First Image"),
            "img2": _("Second Image"),
        }

        help_texts = {
            "description": _("Enter a detailed description of the product."),
            "price": _("Enter the price of the product in numbers only."),
            "summary": _("Write a brief summary of the product."),
        }

        widgets = {
            "catigory": forms.Select(
                attrs={
                    "class": "form-control",
                    "style": "width: 100%; font-size: 18px;",
                }
            ),
            "img1": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "style": "width: 100%; font-size: 18px;",
                }
            ),
            "img2": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "style": "width: 100%; font-size: 18px;",
                }
            ),
        }
