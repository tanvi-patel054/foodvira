from django.urls import path
from apps.store.views import *

urlpatterns = [
    path("", index, name="index"),
    path("products/", products, name="products"),
    path("product_detail/<str:product_id>", product_detail, name="product_detail"),
    path("product-inquiry/", product_inquiry, name="product_inquiry"),
    path("blog/", blog, name="blog"),
    path("blog-detail/<str:blog_id>", blog_detail, name='blog_detail'),
    path("about/", about, name="about"),
    path("contact/", contact, name="contact"),
]