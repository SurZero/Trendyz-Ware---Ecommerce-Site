from django.db import models
from django.conf import settings
from django.shortcuts import reverse
from django.template.defaultfilters import slugify
from django_countries.fields import CountryField
from django.utils import timezone
from django.db.models.signals import pre_save

from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from embed_video.fields import EmbedVideoField

CATEGORY_CHOICES = (
    ('S', 'Shirt'),
    ('P', 'Pants'),
    ('J', 'Jeans'),
    # ('Swtrs', 'Sweaters'),
    ('J&C', 'Jacket and Coats'),
    ('T&Tnks', 'T-shirt and Tanks'),
    ('H&SS', 'Hoodies and Sweatshirts'),
    ('SW', 'Sport Wear'),
)

LABEL_CHOICES = (
    ('P', 'primary'),
    ('S', 'secondary'),
    ('D', 'danger')

)

PAYMENT_CHOICES = (
    ('E', 'eSewa'),
    ('K', 'Khalti'),
    ('C','Cash on Delivery')
)


class Item(models.Model):  # items you can purchase
    image = models.ImageField(default='default.jpg', upload_to='products')
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=10)
    label = models.CharField(choices=LABEL_CHOICES, max_length=1)
    slug = models.SlugField()
    description = RichTextUploadingField()
    date_posted = models.DateTimeField(default=timezone.now)
    video = EmbedVideoField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("items:product", kwargs={'slug': self.slug})

    # def get_category_url(self):
    #     return reverse('items:search_category', kwargs={'category': self.category})

    def get_add_to_cart_url(self):
        return reverse("items:add_to_cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("items:remove_from_cart", kwargs={'slug': self.slug})

    # def save(self, *args, **kwargs):
    #     if not 'rel' in self.video :
    #         self.video = self.video+'?rel=0' 
    #     super(Item, self).save(*args, **kwargs) 

# def pre_save_post_receiver(sender, instance, *args, **kwargs):
#     if not instance.slug:
#         instance.slug = create_slug(instance)
#
#
# pre_save.connect(pre_save_post_receiver, sender=Item)


class OrderItem(models.Model):  # when items added to cart it becomes an Ordered Item
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f'{self.quantity} of {self.item.title}'

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        return self.quantity*self.item.discount_price

    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        else:
            return self.get_total_item_price()


class Order(models.Model):  # as shopping cart
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # associate order with user
    items = models.ManyToManyField(OrderItem)  # so we can add orderItems into order
    ordered = models.BooleanField(default=False)
    start_date = models.DateTimeField(auto_now_add=True)  # moment that order is created
    ordered_date = models.DateTimeField()
    # billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total(self):
        total = 0
        # print(self.items.all())
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total


# class BillingAddress(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     name = models.CharField(max_length=50, null=True, blank=True)
#     phone_number = models.CharField(max_length=11, null=True, blank=True)
#     address = models.CharField(max_length=100)
#     payment_option = models.CharField(choices=PAYMENT_CHOICES, max_length=3, default='C')

#     def __str__(self):
#         return self.user.username

