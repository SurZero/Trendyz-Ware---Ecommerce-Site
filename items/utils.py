from django.utils.text import slugify

import random
import string


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# def create_slug(instance, new_slug=None):
#     slug = slugify(instance.title)
#     if new_slug is not None:
#         slug = new_slug
#     klass = instance.__class__
#     qs = klass.objects.filter(slug=slug).exists()
#     if qs:
#         new_slug = "{slug}-{randstr}".format(
#             slug=slug,
#             randstr=random_string_generator(size=4)
#         )
#         return create_slug(instance, new_slug=new_slug)
#     return slug


