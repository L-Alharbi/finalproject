from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Avg

from django.http import JsonResponse
import json
# Create your views here.



def product(request, pk):
    product = Product.objects.get(id=pk)

    #recommendations based on category
    products = Product.objects.filter(category=product.category).exclude(id=pk)[:1]

    #show reviews
    review = Review.objects.filter(product=product)

    #Avg Rating
    avgRate = Review.objects.filter(product=product).aggregate(rating=Avg('rating'))

    #Review Form
    reviewform = ReviewForm()

    create_review = True

    if request.user.is_authenticated:
        customer = Customer.objects.get(user=request.user)        
        user_review = Review.objects.filter(customer=customer, product=product).count()

        if user_review > 0:
            create_review = False




    context = {
        'create_review':create_review,
        'product':product,
        'products':products,
        'review':review,
        'avgRate':avgRate,
        'reviewform':reviewform,
         }
    
    return render(request, 'store/product.html',context)



def search(request):
    query = request.GET.get('q', '')
    selected_category = request.GET.get('category', '')

    products = Product.objects.filter(name__icontains=query).order_by("-price")
    if selected_category:
        products = products.filter(category__name=selected_category)

    categories = Category.objects.all()
    context = {
        'products': products,
        'query': query,
        'categories': categories,
        'selected_category': selected_category,
    }
    return render(request, 'store/search.html', context)


def category(request, cat ):
    try:
        category = Category.objects.get(name=cat)
        product = Product.objects.filter(category=category)
        return render(request,'store/category.html',{
            'products':product, 
            'category':category, 
            })

    except:
        return redirect('store')

def subcategory_view(request, category_name, subcategory_name):
    category = Category.objects.get(name=category_name)
    subcategory = Subcategory.objects.get(category=category, name=subcategory_name)
    product = Product.objects.filter(subcategory=subcategory)
    

    return render(request, 'store/subcategory.html', {
        'products':product, 
        'category': category, 
        'subcategory': subcategory,
    })

def profile(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request,current_user)
            return redirect('store')
        
        return render(request,'store/profile.html',{'user_form':user_form})

    else:
        messages.success(request, "You must be logged in to access the page.")
        return redirect('store')

def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    context = {'form':form}
    return render(request, 'store/register.html', context)

def loginPage(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('store')
        else:
            pass
    else:
        context = {}
        return render(request, 'store/login.html', context)

def store(request):
    if request.user.is_authenticated:
        user = request.user

        customer, created = Customer.objects.get_or_create(user=user)

        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.cartItems
    else:
        items = []
        order = {'cartTotal': 0, 'cartItems': 0}
        cartItems = order['cartItems']

    categorys = Category.objects.all()
    subcategorys = Subcategory.objects.all()
    products = Product.objects.all() 

    context = {
        'products': products,
        'categorys': categorys,
        'subcategorys': subcategorys,
        'cartItems': cartItems
    }
    return render(request, 'store/store.html', context)

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'cartTotal':0, 'cartItems':0}

    context = {'items':items, 'order':order}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer 
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'cartTotal':0, 'cartItems':0}

    context = {'items':items, 'order':order}    
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('action:',action)
    print('productId:',productId)

    customer = request.user.customer
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


    return JsonResponse('Item added', safe=False)


def ajax_add_review(request, pk, ):
    product = Product.objects.get(id=pk)
    customer = Customer.objects.get(user=request.user)
    #user = request.user


    review = Review.objects.create(
        customer = customer,
        product = product,
        review = request.POST['review'],
        rating = request.POST['rating'],

    )

    context = {
        'customer': customer.user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
    }

    avgRate = Review.objects.filter(product=product).aggregate(rating=Avg('rating'))

    return JsonResponse(
        {
        'bool': True,
        'context': context,
        'avgRate': avgRate
        }
    )


def logoutfunc(request):
    logout(request)
    return redirect('store')