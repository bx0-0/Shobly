from django import forms
from django.utils.translation import gettext_lazy as _
from products.models import Category

class ProductForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"}),
        empty_label=_("Select a category"),
        label=_("Category")
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "placeholder": _("Enter product description")}),
        label=_("Description")
    )
    price_min = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": _("Minimum Price")}),
        label=_("Minimum Price")
    )
    price_max = forms.DecimalField(
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": _("Maximum Price")}),
        label=_("Maximum Price")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['category'].label_from_instance = lambda obj: _(obj.name)
