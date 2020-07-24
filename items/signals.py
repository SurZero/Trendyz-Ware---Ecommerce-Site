from django.db.models.signals import pre_save  # signals that gets fired after objesct is saved
from django.dispatch import receiver
from django.utils.text import slugify

from .models import Item


# @receiver(pre_save, sender=Item)
# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.title)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Item.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" % (slug, qs.first().id)
#         return create_slug(instance, new_slug=new_slug)
#     return slug
#
#
# @receiver(pre_save, sender=Item)
# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)