# from urllib import request

from django import template


from items.models import Order

register = template.Library()  # this is how we register our templatetags


@register.filter()
def cart_item_count(user):
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            # print(f'QS[0]{qs[0]}')
            # print(qs[0].items.count())
            return qs[0].items.count()
        else:
        	print("TEMPLATES EMPTY")
    return 0




