from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order, OrderItem
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

cart = {}

def index(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})

@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    cart.setdefault(request.user.id, {})
    cart[request.user.id][pk] = cart[request.user.id].get(pk, 0) + 1
    return redirect('cart')

@login_required
def cart_view(request):
    user_cart = cart.get(request.user.id, {})
    items = []
    total = 0
    for pid, qty in user_cart.items():
        product = get_object_or_404(Product, pk=pid)
        total += product.price * qty
        items.append({'product': product, 'quantity': qty})
    return render(request, 'cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
    user_cart = cart.get(request.user.id, {})
    if user_cart:
        order = Order.objects.create(user=request.user)
        for pid, qty in user_cart.items():
            product = get_object_or_404(Product, pk=pid)
            OrderItem.objects.create(order=order, product=product, quantity=qty)
        cart[request.user.id] = {}
    return redirect('index')

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('index')
