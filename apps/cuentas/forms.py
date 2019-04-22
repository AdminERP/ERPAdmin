from django import forms

from .models import CuentaPagar, Item, ServiceOrder, CuentaCobrar

class PaymentAccountForm(forms.ModelForm):
    orders = CuentaPagar.ordenesParaContabilizar()
    order = forms.ModelChoiceField(orders)
    def __init__(self, *args, **kwargs):
        super(PaymentAccountForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)

        if instance and instance.pk:
            del self.fields['order']
            del self.fields['invoice']
            del self.fields['supplier_id']
            
    class Meta:
        model = CuentaPagar
        fields = (
    		'total',
            'invoice', 
    		'invoice_date',
    		'term_date',
    		'status',
    		'order',
    		'supplier_id')

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = (
    		'name', 
    		'value')



class ServiceOrderForm(forms.ModelForm):
    status = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-md-6'}))
    sold_service = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    employee_id = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    comments = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    total = forms.DecimalField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    class Meta:
        model = ServiceOrder
        fields = (
            'status', 
            'sold_service',
            'employee_id',
            'comments',
            'total')

class CuentaCobroForm(forms.ModelForm):
    servicio = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))
    tarifa = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control'}))
    costo_total = forms.DecimalField(widget=forms.TextInput(attrs={'class':'form-control'}))
   
    class Meta:
        model = CuentaCobrar
        fields = (
            'servicio', 
            'tarifa',
            'costo_total',
            'estado',
            'fecha_vencimiento',
            'cuenta_empresa',
            'service_order')