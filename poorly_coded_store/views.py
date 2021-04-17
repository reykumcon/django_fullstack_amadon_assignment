from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Sum

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    order_last_price = Order.objects.last().total_price
    order_quantity = Order.objects.aggregate(Sum('quantity_ordered'))['quantity_ordered__sum']
    order_price = Order.objects.aggregate(Sum('total_price'))['total_price__sum']
    context = {
        'last_purchase': order_last_price,
        'quantity': order_quantity,
        'price': order_price
    }
    return render(request, "store/checkout.html", context)

def payment(request):
    if request.method == 'POST':
        product = Product.objects.get(id=request.POST['id'])
        quantity_from_form = int(request.POST['quantity'])
        total_charge = quantity_from_form * float(product.price)
        print("Charging credit card...")
        Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)
        return redirect('/checkout')
    else:
        return redirect('/')