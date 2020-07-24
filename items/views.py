from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, OrderItem, Order, CATEGORY_CHOICES
from django.views.generic import ListView, DetailView, View, TemplateView
from django.utils import timezone
from .forms import CheckoutForm
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from django.http import JsonResponse
import json

# def products(request):
#     context = {
#         'items': Item.objects.all()
#     }
#     return render(request, "product.html", context)
#


class HomeView(ListView):
    model = Item
    template_name = 'home.html'
    context_object_name = 'items'
    # ordering = ['-date_posted']
    paginate_by = 12

    # def get_context_data(self): # see example.html for templatetag
    #     context = super().get_context_data()
    #     categories = [text for value, text in CATEGORY_CHOICES]    
    #     print(categories)
    #     context['categories'] = categories
    #     return context 

class AboutView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'about.html')


class ContactView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'contact.html')


class ItemDetailView(DetailView):
    model = Item
    template_name = 'product.html'

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        suggestions = Item.objects.filter(
            Q(category=self.object.category) & ~Q(slug=self.object.slug)
        ).order_by('-date_posted')[:3]
        # for suggestion in suggestions:
        #     print(f'DATE POSTED = {suggestion.date_posted}')
        context['suggestions'] = suggestions
        return context



class SearchView(View):
    paginate_by = 12

    def get(self, request, *args, **kwargs):
        prices = []
        result_item = []
        # prices.clear()
        # result_item.clear()
        max_price = request.GET.get('max_price')
        if max_price:
            max_price = int(max_price)
            print(f"VALUE = {max_price}")
            items = Item.objects.filter(price__lte=max_price).order_by('-date_posted')
            if items:
                context = {
                    'items': items,
                    'max_price': max_price
                }
                return render(request, 'max_price_searched.html', context)
            else:
                messages.error(request, "No items matches the price")
                return redirect('items:home')
        else:
            messages.error(request, "Please Enter Maximum Price!")
            return redirect('items:home')


class SearchCategoryView(TemplateView):
    model = Item
    template_name = 'category_search.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        category = self.kwargs.get('category')
        print(f"CATEGORY = {category}")
        if category == 'all':
            items = Item.objects.all()
            context = {
                'items': items
            }
        else:
            items = Item.objects.filter(category=category).order_by('date_posted')
            # for item in items:
            #     print(item.category)
            context = {
                'items': items
            }

        return context


class CheckoutView(View):
    def get(self, *args, **kwargs):
        # form

        form = CheckoutForm()
        order = Order.objects.get(user=self.request.user, ordered=False)
        print(order.id, order.items.all(), order.get_total())
        context = {
            'form': form
        }
        return render(self.request, 'checkout-page.html', context)

    # def post(self, *args, **kwargs):
    #     form = CheckoutForm(self.request.POST or None)
    #     print(self.request.POST)
    #     try:
    #         order = Order.objects.get(user=self.request.user, ordered=False)
    #         print('order')
#             print(order.ordered)
#             if form.is_valid():
#                 name = form.cleaned_data.get('name')
#                 phone_number = form.cleaned_data.get('phone_number')
#                 address = form.cleaned_data.get('address')
#                 payment_option = form.cleaned_data.get('payment_option')

#                 billing_address_obj = BillingAddress(
#                     user=self.request.user,
#                     name=name,
#                     phone_number=phone_number,
#                     address=address,
#                     payment_option=payment_option,
#                 )

#                 billing_address_obj.save()
#                 print(f'ADDRESS = {billing_address_obj.address}')
#                 order.billing_address = BillingAddress(address=address)
#                 print(f'BILLING ADDRESS ORDER={order.billing_address.address}')
#                 print(f'ORDER USER ={billing_address_obj.user.id}')
#                 # order.billing_address.save()
#                 order.ordered = True
#                 order.save()
#                 # print(form.cleaned_data)
#                 print('Forms is valid')
#                 messages.success(self.request, 'Success')
#                 return redirect('items:checkout')
#             else:
#                 print("CHECKOUT FAILED!!!")
#                 messages.warning(self.request, 'Failed Checkout')
#                 # raise ValidationError([
#                 #     ValidationError(_('Error 1'), code='error1'),
#                 #     ValidationError(_('Error 2'), code='error2'),
#                 # ])
#                 return redirect("items:checkout")

#         except ObjectDoesNotExist:
#             messages.error(self.request, 'You do not have an active order')
#             return redirect('items:order_summery')


class Payment(View):

    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        context = {
            'order': order
        }
        return render(self.request, 'payment.html')


class OrderSummeryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': order
            }
            return render(self.request, 'order_summery.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, 'You do not have an active order')
            return redirect('/')


@login_required()
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)  # for ex item 1... obj of Item with current item
    # print(f'item after get {item}') #prints current item
    # print(f'item.price ={item.price}') #prints current item price
    order_item, created = OrderItem.objects.get_or_create(  # returns tuples
        item=item,
        user=request.user,
        ordered=False
    )  # creates OrderItem which returns self.quantity of self.item.title-- see OrderItem model
    # print('/n')
    print(order_item)
    order_qs = Order.objects.filter(  # to check if the order is already exists
        user=request.user,
        ordered=False
    )  # gives which isn't ordered!
    # print(f'order query set = {order_qs}') prints: <QuerySet [<Order: susil>]>

    if order_qs.exists():  # if order is already exists/if the user has order
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, f"{order_item.item.title} quantity is updated!")
            # return redirect("items:product", slug=slug)

        else:
            order.items.add(order_item)
            messages.info(request, f"{order_item.item.title} is added to your cart.")
            # return redirect("items:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, f"{order_item.item.title} is added to your cart.")
       
    return redirect("items:product", slug=slug)

# def cart_item_count(user):
#     if user.is_authenticated:
#         qs = Order.objects.filter(user=user, ordered=False)
#         if qs.exists():
#             # print(f'QS[0]{qs[0]}')
#             # print(qs[0].items.count())
#             return qs[0].items.count()
#         else:
#         	print("TEMPLATES EMPTY")
#     return 0


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)  # takes Item creates OrderItem and assigns order_item to order if user
    # hasn't order
    # checking if user has order
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )

    if order_qs.exists():
        order = order_qs[0]
        # print(f'ORDER.....={order}')
        if order.items.filter(item__slug=item.slug).exists():  # check if user has order
            order_item = OrderItem.objects.filter(  # if true? then grab order_item
                item=item,
                user=request.user,
                ordered=False
            )[0]
            # print('INSIDE IF ....')
            print(f'order item= {order_item}')

            # order_item.quantity -= 1
            # order.items.remove(order_item)
            order_item.delete()
            messages.success(request, f"{order_item.item.title} was removed from your cart.")
            return redirect("items:order_summery")
            # print('order item deleted!!!')

            # order_item.save()

        else:
            # print('INSIDE MIDDLE ELSE.....')
            messages.info(request, "This item is not in your cart.")
            return redirect("items:product", slug=slug)
    else:
        # print('INSIDE LAST ELSE ....')
        messages.info(request, "You do not have an active order.")
        return redirect("items:product", slug=slug)

    # return redirect("items:product", slug=slug)


@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Item,
                             slug=slug)  # takes Item creates OrderItem and assigns order_item to order if user
    # hasn't order
    # checking if user has order
    order_qs = Order.objects.filter(
        user=request.user,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        order_item = OrderItem.objects.filter(  # if true? then grab order_item
            item=item,
            user=request.user,
            ordered=False
        )[0]
        if order.items.filter(item__slug=item.slug).exists():  # check if user has order
            # print('inside if')
            # print(f'order item= {order_item}')

            # order_item.quantity -= 1
            # order.items.remove(order_item)
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, f"{order_item.item.title} quantity was updated.")
            return redirect("items:order_summery")
            # print('order item deleted!!!')

            # order_item.save()

        else:
            print(" inside else")
            messages.info(request, f"{order_item.item.title} is not in your cart.")
            return redirect("items:product", slug=slug)
    else:
        messages.info(request, "You do not have an active order.")
        return redirect("items:product", slug=slug)

    # return redirect("items:product", slug=slug)

@login_required
def updateItem(request):
    data = json.loads(request.body)
    # print(f"POST DATA = {request.POST['productSlug']}")

    slug = data['productSlug']
    action = data['action']
    print(f"SLUGGG= {slug}")

    item = Item.objects.get(slug=slug)

    order_qs = Order.objects.filter(  # to check if the order is already exists
    user=request.user,
    ordered=False
    )  # gives which isn't ordered!
    # print(f'order query set = {order_qs}') prints: <QuerySet [<Order: susil>]>


    if action == 'add':
        order_item, created = OrderItem.objects.get_or_create(  # returns tuples
            item=item,
            user=request.user,
            ordered=False
        )

        if order_qs.exists():  # if order is already exists/if the user has order
            order = order_qs[0]
            # check if the order item is in the order
            if order.items.filter(item__slug=item.slug).exists():
                order_item.quantity += 1
                order_item.save()
                data = {'count': Order.objects.filter(user=request.user, ordered=False)[0].items.count(),
                    'messages': "quantity updated"
                }
                return JsonResponse(data, safe=False)

            else:
                order.items.add(order_item)
                data = {'count': Order.objects.filter(user=request.user, ordered=False)[0].items.count(),
                    'messages': "added to cart"
                    }
                return JsonResponse(data, safe=False)
        else:
            ordered_date = timezone.now()
            order = Order.objects.create(user=request.user, ordered_date=ordered_date)
            order.items.add(order_item)
            data = {'count': Order.objects.filter(user=request.user, ordered=False)[0].items.count(),
                    'messages': "added to cart"
                }

            return JsonResponse(data, safe=False)

    elif action == 'remove':
        if order_qs.exists():
            order = order_qs[0]
            # print(f'ORDER.....={order}')
            if order.items.filter(item__slug=item.slug).exists():  # check if user has order
                order_item = OrderItem.objects.filter(  # if true? then grab order_item
                    item=item,
                    user=request.user,
                    ordered=False
                )[0]

                order_item.delete()
                data = {'count': Order.objects.filter(user=request.user, ordered=False)[0].items.count(),
                        'messages': "Item is removed from the cart."
                }
                return JsonResponse(data, safe=False)
                

            else:
                data = {'count': Order.objects.filter(user=request.user, ordered=False)[0].items.count(),
                        'messages': "This item is not in your the cart."
                }
                return JsonResponse(data, safe=False)
                
        else:
            # print('INSIDE LAST ELSE ....')
            data = {'count': Order.objects.filter(user=request.user, ordered=False)[0].items.count(),
                    'messages': "You donot have an active order."
                }
            return JsonResponse(data, safe=False)
            

