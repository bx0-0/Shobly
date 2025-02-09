from django_filters import FilterSet
from .models import Cart
import django_filters


class CartFilter(FilterSet):
    product__title = django_filters.CharFilter(
        lookup_expr="icontains",
    )

    class Meta:
        model = Cart
        fields = ["product__title", "quantity"]
