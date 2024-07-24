from django.shortcuts import render, get_object_or_404, redirect
from .models import Invoice, Item, Client
from .forms import InvoiceForm, ItemForm, ClientForm

def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})

def invoice_detail(request, pk):
    try:
        invoice = get_object_or_404(Invoice, pk=pk)
        return render(request, 'invoices/invoice_detail.html', {'invoice': invoice})
    except:
      print('An exception occurred')
   

def invoice_create(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = InvoiceForm()
    return render(request, 'invoices/invoice_form.html', {'form': form})

def item_create(request, invoice_id):
    invoice = get_object_or_404(Invoice, pk=invoice_id)
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.invoice = invoice
            item.save()
            return redirect('invoice_detail', pk=invoice.pk)
    else:
        form = ItemForm()
    return render(request, 'invoices/item_form.html', {'form': form, 'invoice': invoice})
