from django.shortcuts import render
from .models import *
# Create your views here.
def store(request):
    products=Product.objects.all()
    content={'products':products}
    return render(request,'myapp/store.html',content)

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'grand_total':0}
    content={'items':items,'order':order}
    return render(request,'myapp/cart.html',content)

def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else:
        items=[]
        order={'grand_total':0}
    content={'items':items,'order':order}
    return render(request,'myapp/checkout.html',content)

