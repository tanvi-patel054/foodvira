from django.contrib import admin
from apps.products.models import Category, Unit, Product, ProductImages, ProductInquiry
from django.utils.html import format_html
# Register your models here.

# ============================
# INLINE FOR PRODUCT IMAGES
# ============================
class ProductImagesInline(admin.TabularInline):
    model = ProductImages
    extra = 1
    fields = ("image", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


# ============================
# CATEGORY ADMIN
# ============================
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20


# ============================
# UNIT ADMIN
# ============================
@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ("name", "symbol", "created_at")
    search_fields = ("name", "symbol")
    ordering = ("name",)
    list_per_page = 20


# ============================
# PRODUCT ADMIN
# ============================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "unit",
        "price",
        "stock",
        "main_image_preview",
        "created_at"
    )

    list_filter = (
        "category",
        "unit",
        "created_at"
    )

    search_fields = (
        "title",
        "content"
    )

    ordering = ("-created_at",)
    list_per_page = 25

    readonly_fields = (
        "main_image_preview",
        "created_at",
        "updated_at"
    )

    inlines = [ProductImagesInline]

    fieldsets = (
        ("Basic Information", {
            "fields": (
                "category",
                "unit",
                "title",
                "content"
            )
        }),
        ("Product Media", {
            "fields": (
                "image",
                "main_image_preview"
            )
        }),
        ("Pricing & Stock", {
            "fields": (
                "price",
                "stock"
            )
        }),
        ("Additional Details", {
            "fields": (
                "additional_details",
            )
        }),
        ("System Info", {
            "fields": (
                "created_at",
                "updated_at"
            )
        }),
    )

    def main_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="120" height="120" style="object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )
        return "No Image"

    main_image_preview.short_description = "Main Image Preview"


# ============================
# PRODUCT IMAGES ADMIN
# (Optional – Separate control)
# ============================
@admin.register(ProductImages)
class ProductImagesAdmin(admin.ModelAdmin):
    list_display = ("product", "image_preview", "created_at")
    search_fields = ("product__title",)
    list_filter = ("created_at",)
    readonly_fields = ("image_preview",)
    list_per_page = 30

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Preview"


# ============================
# PRODUCT INQUIRY ADMIN
# ============================
@admin.register(ProductInquiry)
class ProductInquiryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "mobile",
        "product",
        "quantity",
        "status",
        "priority",
        "created_at"
    )

    list_filter = (
        "status",
        "priority",
        "created_at"
    )

    search_fields = (
        "name",
        "mobile",
        "product__title",
        "message"
    )

    ordering = ("-created_at",)
    list_per_page = 30

    fieldsets = (
        ("Customer Details", {
            "fields": (
                "name",
                "mobile"
            )
        }),
        ("Product Inquiry", {
            "fields": (
                "product",
                "quantity",
                "message"
            )
        }),
        ("Business Tracking", {
            "fields": (
                "status",
                "priority"
            )
        }),
        ("System Info", {
            "fields": (
                "created_at",
            )
        }),
    )

    readonly_fields = ("created_at",)
