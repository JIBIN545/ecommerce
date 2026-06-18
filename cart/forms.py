from shop import forms

from cart.models import Order
from django import forms
class Checkoutform(forms.ModelForm):
    payment_choices=(('COD','COD' ),('ONLINE','ONLINE'),)
    payment_method=forms.ChoiceField(choices=payment_choices)
    class Meta:
        model = Order
        fields=['address','phone','payment_method']