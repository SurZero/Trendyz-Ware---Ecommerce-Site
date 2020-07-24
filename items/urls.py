from django.urls import path
from .views import (
    HomeView,
    AboutView,
    SearchCategoryView,
    ContactView,
    SearchView,
    ItemDetailView,
    add_to_cart,
    remove_from_cart,
    OrderSummeryView,
    remove_single_item_from_cart,
    Payment,
    CheckoutView,
    updateItem
)

app_name = 'items'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('category_search/<category>/', SearchCategoryView.as_view(), name='search_category'),
    path('search/', SearchView.as_view(), name='search'),
    path('order_summery/', OrderSummeryView.as_view(), name='order_summery'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add_to_cart/<slug>/', add_to_cart, name='add_to_cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('remove_from_cart/<slug>/', remove_from_cart, name='remove_from_cart'),
    path('remove_single_item_from_cart/<slug>/', remove_single_item_from_cart, name='remove_single_item_from_cart'),
    path('payment/<payment_option>/', Payment.as_view(), name='payment'),

    path('update_item/', updateItem, name='update_item'),

]