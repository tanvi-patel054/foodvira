from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from apps.master.models import Blog
import os

from .models import Product, ProductImages


def delete_old_file(instance, field_name):
    """
    Deletes old file when updating with new file
    """
    if not instance.pk:
        return

    try:
        old_instance = instance.__class__.objects.get(pk=instance.pk)
    except instance.__class__.DoesNotExist:
        return

    old_file = getattr(old_instance, field_name)
    new_file = getattr(instance, field_name)

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


@receiver(pre_save, sender=Product)
def product_image_update(sender, instance, **kwargs):
    delete_old_file(instance, "image")


@receiver(pre_save, sender=ProductImages)
def product_gallery_image_update(sender, instance, **kwargs):
    delete_old_file(instance, "image")


@receiver(post_delete, sender=Product)
def product_image_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)


@receiver(post_delete, sender=ProductImages)
def product_gallery_image_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)

@receiver(pre_save, sender=Blog)
def blog_image_update(sender, instance, **kwargs):
    if not instance.pk:
        return

    old = Blog.objects.filter(pk=instance.pk).first()
    if old and old.image and old.image != instance.image:
        if os.path.isfile(old.image.path):
            os.remove(old.image.path)


@receiver(post_delete, sender=Blog)
def blog_image_delete(sender, instance, **kwargs):
    if instance.image and os.path.isfile(instance.image.path):
        os.remove(instance.image.path)