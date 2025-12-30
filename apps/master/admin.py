from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import slugify

from apps.master.models import (
    Contact,
    BlogCategory,
    Blog,
    TeamMember
)

# =========================
# CONTACT ADMIN
# =========================
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("name", "email", "message")
    ordering = ("-created_at",)
    list_per_page = 25

    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Contact Details", {
            "fields": ("name", "email", "message")
        }),
        ("Status", {
            "fields": ("status",)
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at")
        }),
    )


# =========================
# BLOG CATEGORY ADMIN
# =========================
@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active", "created_at")
    search_fields = ("name",)
    ordering = ("name",)
    list_per_page = 20

    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Category Info", {
            "fields": ("name", "slug", "description")
        }),
        ("Status", {
            "fields": ("is_active",)
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at")
        }),
    )


# =========================
# BLOG ADMIN
# =========================
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "image_preview",
        "created_at"
    )

    list_filter = ("category", "created_at")
    search_fields = ("title", "content")
    ordering = ("-created_at",)
    list_per_page = 20

    readonly_fields = (
        "image_preview",
        "created_at",
        "updated_at"
    )

    prepopulated_fields = {"slug": ("title",)}

    fieldsets = (
        ("Blog Details", {
            "fields": ("category", "title", "slug", "content")
        }),
        ("Featured Image", {
            "fields": ("image", "image_preview")
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="120" height="120" style="object-fit:cover;border-radius:8px;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Image Preview"


# =========================
# TEAM MEMBER ADMIN
# =========================
@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "position",
        "order",
        "image_preview"
    )

    list_filter = ("position",)
    search_fields = ("name", "position", "bio")
    ordering = ("order", "name")
    list_per_page = 25

    readonly_fields = (
        "image_preview",
        "created_at",
        "updated_at"
    )

    fieldsets = (
        ("Basic Information", {
            "fields": ("name", "position", "bio")
        }),
        ("Profile Image", {
            "fields": ("image", "image_preview")
        }),
        ("Social Media Links", {
            "fields": (
                "facebook_url",
                "twitter_url",
                "instagram_url",
                "linkedin_url"
            )
        }),
        ("Display Settings", {
            "fields": ("order",)
        }),
        ("System Info", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="80" height="80" style="object-fit:cover;border-radius:50%;" />',
                obj.image.url
            )
        return "No Image"

    image_preview.short_description = "Profile Image"
