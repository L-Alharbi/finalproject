from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),\
    path('profile/', views.profile, name="profile"),
    path('update_Item/', views.updateItem, name="update_Item"),


]