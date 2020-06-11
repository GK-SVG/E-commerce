from django.shortcuts import render

# Create your views here.
def store(request):
    content={}
    return render(request,'myapp/store.html',content)

def cart(request):
    content={}
    return render(request,'myapp/cart.html',content)

def checkout(request):
    content={}
    return render(request,'myapp/checkout.html',content)


