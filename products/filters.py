import django_filters
from .models import Category, Product


class ProductFilter(django_filters.FilterSet):

    title = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        widget=django_filters.widgets.forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Search by title"}
        ),
    )

    category = django_filters.ModelChoiceFilter(
        queryset=Category.objects.all(),
        widget=django_filters.widgets.forms.Select(
            attrs={"class": "form-control", "placeholder": "Select category"}
        ),
    )

    class Meta:
        model = Product

        fields = ["title", "catigory"]
