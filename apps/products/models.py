from django.db import models
from apps.master.models import BaseClass, upload_with_uuid
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
import os


class Category(BaseClass):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Unit(BaseClass):
    name = models.CharField(max_length=200)
    symbol = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.symbol if self.symbol else self.name


class Product(BaseClass):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products"
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.SET_NULL,
        null=True,
        related_name="products"
    )

    image = models.ImageField(upload_to=upload_with_uuid)
    title = models.CharField(max_length=255)
    content = models.TextField(blank=True, null=True)

    additional_details = models.JSONField(
        blank=True,
        null=True,
        default=dict
    )

    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title


class ProductImages(BaseClass):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to=upload_with_uuid)

    def __str__(self):
        return f"{self.product.title} Image"

class ProductInquiry(BaseClass):
    STATUS_CHOICES = (
        ("new", "New"),
        ("contacted", "Contacted"),
        ("quoted", "Quoted"),
        ("follow_up", "Follow Up"),
        ("converted", "Converted"),
        ("closed", "Closed"),
    )

    PRIORITY_CHOICES = (
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
    )
      # 📊 Business Tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new"
    )
    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium"
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="inquiries"
    )
    name = models.CharField(max_length=150)
    mobile = models.CharField(max_length=20)
    quantity = models.CharField(max_length=100, blank=True, null=True)
    message = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry - {self.product.title} ({self.name})"
    