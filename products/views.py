from django.shortcuts import redirect, render
from .models import Product, Category
from .forms import ProductForm
from accounts.models import Profile
from django.db.models import Avg, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .filters import ProductFilter
from django.contrib import messages


def create_product(request):

    profile = Profile.objects.get(user=request.user)

    if not profile.paypal_email:
        messages.error(
            request,
            "You need to add a PayPal email to your profile before creating a product.",
        )
        return redirect("accounts:edit-profile")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():

            product = form.save(commit=False)
            product.user = request.user
            product.save()

            return redirect("products:product_detail", slug=product.slug)
    else:

        form = ProductForm()

    return render(request, "create_product.html", {"form": form})


def product_detail(request, slug):

    product = Product.objects.get(slug=slug)

    user = product.user

    user_img = Profile.objects.get(user=user).ProfileImg

    company_name = Profile.objects.get(user=user).company_name

    related_products = (
        Product.objects.filter(catigory=product.catigory)
        .exclude(slug=slug)
        .annotate(avg_rating=Avg("ratings__rating"))
        .order_by("-avg_rating")
    )

    product_rate_avg = product.ratings.aggregate(Avg("rating"))

    if product_rate_avg["rating__avg"] is None:
        product_rate_avg["rating__avg"] = 0

    ratings_count = (
        product.ratings.values("rating")
        .annotate(count=Count("rating"))
        .order_by("-rating")
    )

    number_of_rater = product.ratings.count()

    return render(
        request,
        "product_detail.html",
        {
            "product": product,
            "user_img": user_img,
            "company_name": company_name,
            "ratings_count": ratings_count,
            "related_products": related_products,
            "product_rate_avg": product_rate_avg,
            "number_of_rater": number_of_rater,
            "int_avg_rate": range(0, int(product_rate_avg["rating__avg"])),
        },
    )


def product_list(request):

    products = Product.objects.filter(amount__gt=0)

    product_filter = ProductFilter(request.GET, queryset=products)
    filtered_products = product_filter.qs

    paginator = Paginator(filtered_products, 10)
    page = request.GET.get("page")
    try:
        paginated_products = paginator.page(page)
    except PageNotAnInteger:

        paginated_products = paginator.page(1)
    except EmptyPage:

        paginated_products = paginator.page(paginator.num_pages)

    categories = Category.objects.all()

    return render(
        request,
        "product_list.html",
        {
            "products": paginated_products,
            "filter": product_filter,
            "categories": categories,
        },
    )


def delete_product(request, slug):

    product = Product.objects.get(slug=slug, user=request.user)

    product.delete()

    return redirect("products:user_products")


def edit_product(request, slug):
    product = Product.objects.get(slug=slug, user=request.user)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            return redirect("products:product_detail", slug=product.slug)
    else:
        form = ProductForm(instance=product)

    return render(request, "create_product.html", {"form": form})


def user_products(request):

    product_filter = ProductFilter(
        request.GET, queryset=Product.objects.filter(user=request.user)
    )

    filtered_products = product_filter.qs

    paginator = Paginator(filtered_products, 5)
    page = request.GET.get("page")
    try:

        products = paginator.page(page)
    except PageNotAnInteger:

        products = paginator.page(1)
    except EmptyPage:

        products = paginator.page(paginator.num_pages)

    return render(
        request, "user_products.html", {"products": products, "filter": product_filter}
    )
