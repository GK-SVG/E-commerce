from django.urls import path
from .import views


urlpatterns = [
    path('',views.store,name='store'),
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout') ,  
    path('update_item',views.updateItem,name='UpdateItem'),
    path('processOrder',views.processOrder,name='ProcessOrder'),
    path("handlerequest/", views.handlerequest, name="HandleRequest"),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('orders/',views.orders,name='order'),
    path('orderitems/<int:id>/',views.orderitems,name='orderitems'),
]