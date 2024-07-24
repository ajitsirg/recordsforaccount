from django import forms
from .models import Invoice, Item, Client

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'phone']

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['client', 'due_date', 'paid']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['description', 'quantity', 'price']
