from django.contrib import messages
from accounts.models import Profile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from products.models import Product
from .models import Cart, FailedOrder
from .filters import CartFilter
import json
from django.http import JsonResponse
from .models import Order, OrderItem
from .helper_function import send_product_details_to_shipping_company, send_payout
from django.db import transaction
from django.contrib.auth.decorators import user_passes_test


def cart(request):

    cart = Cart.objects.filter(user=request.user)

    cart_filter = CartFilter(request.GET, queryset=cart)

    paypal_email = Profile.objects.get(user=request.user).paypal_email

    return render(
        request,
        "cart.html",
        {"cart": cart_filter.qs, "filter": cart_filter, "paypal_email": paypal_email},
    )


def add_to_cart(request, slug):
    if request.method == "POST":

        product = Product.objects.get(slug=slug)

        cart = Cart.objects.filter(user=request.user, product=product)

        if cart.exists():

            cart = Cart.objects.get(user=request.user, product=product)
            if cart.quantity < product.amount:
                cart.quantity += 1
                cart.save()
        else:

            if product.amount > 0:

                cart = Cart(user=request.user, product=product, quantity=1)
                cart.save()

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect(request.META.get("HTTP_REFERER"))


def remove_from_cart(request, slug):
    if request.method == "POST":

        product = Product.objects.get(slug=slug)

        Cart.objects.filter(user=request.user, product=product).delete()

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect(request.META.get("HTTP_REFERER"))


def increase_quantity(request, slug):
    if request.method == "POST":

        product = Product.objects.get(slug=slug)

        cart = Cart.objects.get(user=request.user, product=product)

        if cart.quantity < product.amount:

            cart.quantity += 1
            cart.save()
        else:

            return HttpResponse("The quantity is more than the stock", status=400)

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect(request.META.get("HTTP_REFERER"))


def decrease_quantity(request, slug):
    if request.method == "POST":

        product = Product.objects.get(slug=slug)

        cart = Cart.objects.get(user=request.user, product=product)

        if cart.quantity <= 1:

            cart.delete()
        else:

            cart.quantity -= 1
            cart.save()

        return redirect(request.META.get("HTTP_REFERER"))

    return redirect(request.META.get("HTTP_REFERER"))


@transaction.atomic
def complete_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        transaction_id = data.get("transactionId")
        product_slug = data.get("productSlug")
        quantity = data.get("Quantity")
        total_price = data.get("TotalPrice")

        product = Product.objects.get(slug=product_slug)

        if quantity.isdigit():
            product.amount -= float(quantity)
            product.save()
        else:
            return JsonResponse({"error": "Invalid quantity value"}, status=400)

        order = Order(user=request.user, order_number=transaction_id)
        order.save()

        order_item = OrderItem(
            order=order, product=product, quantity=quantity, total_price=total_price
        )
        order_item.save()

        Cart.objects.filter(user=request.user, product=product).delete()

        buyer_email = request.user.email
        seller_email = product.user.email
        paypal_seller_email = Profile.objects.get(user=product.user).paypal_email
        order_details = {
            "order_number": transaction_id,
            "product_name": product.title,
            "quantity": quantity,
            "total_price": total_price,
            "order_status": "Pending",
            "order_id": order.slug,
        }
        res = send_product_details_to_shipping_company(
            order_details, buyer_email, seller_email
        )

        if res[0] == 200 and res[1] == "Shipped":
            order.order_status = "Shipped"
            order.save()

            commission_rate = 0.01
            paypal_fee_rate = 0.029
            fixed_fee = 0.30

            commission = float(total_price) * commission_rate

            seller_amount = float(total_price) - commission

            paypal_fee = (seller_amount * paypal_fee_rate) + fixed_fee

            payout = seller_amount - paypal_fee

            respon = send_payout(paypal_seller_email, payout, currency="USD")
            return JsonResponse(
                {
                    "message": "Order completed successfully and product is being shipped"
                },
                status=200,
            )
        else:

            failed_order = FailedOrder(
                order=order,
                product=product,
                quantity=order_item.quantity,
                total_price=order_item.total_price,
                shipping_response=res,
            )
            failed_order.save()
            order.order_status = "Failed"
            order.save()
            return JsonResponse(
                {
                    "error": "Failed to send product details to shipping company please contact our team"
                },
                status=500,
            )
    return JsonResponse({"error": "Invalid request method"}, status=400)


@user_passes_test(lambda u: u.is_superuser)
def refund_failed_order(request, id):
    failed_order = get_object_or_404(FailedOrder, id=id)
    user = failed_order.order.user
    paypal_email = Profile.objects.get(user=user).paypal_email
    print(paypal_email, failed_order.total_price)
    respon = send_payout(paypal_email, failed_order.total_price, currency="USD")
    print(respon)
    if "ERROR" not in respon:
        failed_order.delete()
    messages.success(request, f"response: {respon}")
    return HttpResponseRedirect("/admin/cart/failedorder/")
