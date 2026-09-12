from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Product, Order, OrderItem


def product_list(request):
    products = Product.objects.all()
    return render(request, 'store/product_list.html', {'products': products})


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    return render(
        request,
        'store/product_detail.html',
        {'product': product}
    )
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1
    else:
        cart[product_id] = 1

    request.session['cart'] = cart

    return redirect('cart')
def cart_view(request):
    cart = request.session.get('cart', {})

    cart_items = []
    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        item_total = product.price * quantity
        total += item_total

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    return render(
        request,
        'store/cart.html',
        {
            'cart_items': cart_items,
            'total': total
        }
    )
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})

    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]

    request.session['cart'] = cart

    return redirect('cart')

def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        cart[product_id] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        if cart[product_id] > 1:
            cart[product_id] -= 1
        else:
            del cart[product_id]

    request.session['cart'] = cart
    return redirect('cart')

from django.contrib.auth import login
from django.shortcuts import redirect


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        User.objects.create_user(
            username=username,
            password=password
        )

        return redirect('login')

    return render(request, 'store/register.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            return redirect('product_list')

        return render(
            request,
            'store/login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'store/login.html')
def user_logout(request):
    logout(request)
    return redirect('product_list')

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')

    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    total = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)
        total += product.price * quantity

    if request.method == 'POST':
        name = request.POST['name']
        address = request.POST['address']
        phone = request.POST['phone']

        order = Order.objects.create(
            user=request.user,
            name=name,
            address=address,
            phone=phone,
            total=total
        )

        for product_id, quantity in cart.items():
            product = get_object_or_404(
                Product,
                id=product_id
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.price
            )

        request.session['cart'] = {}

        return redirect('order_success')

    return render(
        request,
        'store/checkout.html',
        {
            'cart': cart,
            'total': total
        }
    )

def order_success(request):
    return render(
        request,
        'store/order_success.html'
    )
def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('login')

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'store/my_orders.html',
        {'orders': orders}
    )