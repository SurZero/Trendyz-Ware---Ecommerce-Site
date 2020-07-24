from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget

PAYMENT_CHOICES = (
    ('E', 'eSewa'),
    ('K', 'Khalti'),
    ('C','Cash on Delivery')
)


class CheckoutForm(forms.Form):
    name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=11)
    address = forms.CharField()
    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
