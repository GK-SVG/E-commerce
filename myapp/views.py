from django.shortcuts import render,redirect
from django.http import JsonResponse
import json
from .models import * 
import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm
from django.views.decorators.csrf import csrf_exempt
from Paytm import Checksum
#last commit changed
MERCHANT_KEY = 'MJs5tlGfwOMzMTQ@'
#@login_required(login_url='login')
def store(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.grand_total
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'grand_total':0}
		cartItems = order['grand_total']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems,'items':items}
	return render(request, 'myapp/store.html', context)

@login_required(login_url='login')
def cart(request):

	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.grand_total
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'get_cart_items':0}
		cartItems = order.grand_total

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'myapp/cart.html', context)



#@login_required(login_url='login')
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

@login_required(login_url='login')
def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	if request.user.is_authenticated:
		customer = request.user
		email=request.POST.get('email')
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		total = order.get_cart_items
		order.transaction_id = transaction_id
		order.complete=True
		order.save()
		ShippingAddress.objects.create(
			customer=customer,
			order=order,
			address=request.POST.get('address'),
			city=request.POST.get('city'),
			state=request.POST.get('state'),
			zipcode=request.POST.get('zipcode'),
			)
		param_dict={
			    
				'MID': 'toaldV34834751882298',
                'ORDER_ID': str(transaction_id),
                'TXN_AMOUNT': str(total),
                'CUST_ID': email,
                'INDUSTRY_TYPE_ID': 'Retail',
                'WEBSITE': 'WEBSTAGING',
                'CHANNEL_ID': 'WEB',
                'CALLBACK_URL':'http://gk-e-shop.herokuapp.com/handlerequest/',
		}
		param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, MERCHANT_KEY)
		return render(request,'myapp/paytm.html',{'param_dict':param_dict})		
	else:
		print('User is not logged in')

	return redirect('')

@csrf_exempt
def handlerequest(request):
    # paytm will send you post request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            checksum = form[i]

    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order success full')
        else:
            #order_success=messages.error(request,f'order was not successful because {response_dict[RESPMSG]}')
            print('order was not successful because' + response_dict['RESPMSG'])
    return render(request, 'myapp/paymentstatus.html', {'response': response_dict})


@login_required(login_url='login')
def checkout(request):
	if request.user.is_authenticated:
		customer = request.user
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
		items = order.orderitem_set.all()
		cartItems = order.grand_total
	else:
		#Create empty cart for now for non-logged in user
		items = []
		order = {'get_cart_total':0, 'grand_total':0}
		cartItems = order.grand_total

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'myapp/checkout.html', context)


def registerPage(request):
	if request.user.is_authenticated:
		return redirect('/')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)
				return redirect('/')
		context = {'form':form}
		return render(request, 'myapp/register.html', context)
        
	
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, 'Username OR password is incorrect')
        context = {}
        return render(request, 'myapp/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('/')