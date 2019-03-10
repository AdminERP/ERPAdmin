from django import forms

from .models import CuentaPagar, Item, ServiceOrder

class PaymentAccountForm(forms.ModelForm):
    class Meta:
        model = CuentaPagar
        fields = (
    		'total', 
    		'invoice_date',
    		'term_date',
    		'status',
    		'order_id',
    		'supplier_id')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
    		'name', 
    		'value')



class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = (
            'status', 
            'sold_service',
            'employee_id',
            'comments',
            'total')