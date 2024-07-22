from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name="store"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),

    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutfunc, name="login"),
    path('register/', views.registerPage, name="register"),

    path('profile/', views.profile, name="profile"),
    #path('update_password/', views.update_password, name="update_password"),




    path('update_Item/', views.updateItem, name="update_Item"),
    path('category/<str:cat>', views.category, name="category"),
    path('category/<str:category_name>/subcategory/<str:subcategory_name>/', views.subcategory_view, name='subcategory'),

    

    path('search/', views.search, name="search"),
    path('product/<int:pk>', views.product, name="product"),

    path('ajax_add_review/<int:pk>', views.ajax_add_review, name="ajax_add_review"),



]