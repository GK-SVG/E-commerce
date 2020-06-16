from django.urls import path
from .import views


urlpatterns = [
    path('',views.store,name='store'),
    path('cart',views.cart,name='cart'),
    path('checkout',views.checkout,name='checkout') ,  
    path('update_item',views.updateItem,name='UpdateItem'),
    path('process_order',views.processOrder,name='ProcessOrder'),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
]