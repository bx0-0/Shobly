from django.db import models
import uuid


class Cart(models.Model):

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.product.title} - {self.quantity}"


class Order(models.Model):

    user = models.ForeignKey("auth.User", on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    order_number = models.CharField(max_length=50, unique=True)
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Shipped", "Shipped"),
        ("Failed", "Failed"),
    ]

    order_status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default="Pending"
    )

    slug = models.SlugField(unique=True, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = f"{self.user.username}-{uuid.uuid4()}"
        return super().save(*args, **kwargs)


class OrderItem(models.Model):

    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="order_items"
    )

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    quantity = models.PositiveIntegerField()

    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Total Price"
    )

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"


class FailedOrder(models.Model):

    order = models.ForeignKey(
        "Order", on_delete=models.CASCADE, related_name="failed_order_items"
    )

    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)

    shipping_response = models.TextField()

    quantity = models.PositiveIntegerField()

    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Total Price"
    )

    def __str__(self):
        return f"{self.product.title} - {self.quantity}"
