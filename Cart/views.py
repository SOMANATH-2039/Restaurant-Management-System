from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem,Order,OrderItem
from Menu.models import MenuItems  # Assuming a Product model exists
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.urls import reverse

# Check if user is a superuser
def superuser_required(user):
    return user.is_superuser


def get_cart(request):
    """Helper function to retrieve or create a cart for the user or session."""
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
        cart, created = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def add_to_cart(request, product_id):
    """Add product to cart or update quantity."""
    product = get_object_or_404(MenuItems, id=product_id)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1  # If item already exists, increase the quantity
    cart_item.save()

    messages.success(request, f'Added {product.name} to your cart.')
    return redirect('cart_detail')


def update_cart(request, cart_item_id):
    """Update the quantity of an item in the cart."""
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, f'Updated {cart_item.product.name} quantity to {quantity}.')
        else:
            cart_item.delete()
            messages.success(request, f'Removed {cart_item.product.name} from your cart.')

    return redirect('cart_detail')


def remove_from_cart(request, cart_item_id):
    """Remove an item from the cart."""
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    messages.success(request, f'Removed {cart_item.product.name} from your cart.')
    cart_item.delete()
    return redirect('cart_detail')


def cart_detail(request):
    """View to display cart details."""
    cart = get_cart(request)
    return render(request, 'cart_detail.html', {'cart': cart})

@login_required
def checkout(request):
    """Checkout view to handle order creation and redirect to payment."""
    cart = get_cart(request)
    if not cart.cart_items.exists():
        messages.error(request, "Your cart is empty!")
        return redirect('cart_detail')

    # Create a new order
    order = Order.objects.create(
        user=request.user,
        total_price=cart.total_price,
        is_paid=False
    )

    # Create order items from the cart items
    for cart_item in cart.cart_items.all():
        OrderItem.objects.create(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            price=cart_item.product.price    #Changed because OrderItem.price is changed to its property
        )

    # Redirect to payment processing
    return redirect('process_payment', order_id=order.id)


@login_required
def order_detail(request, order_id):
    """Displays the details of a specific order."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_detail.html', {'order': order})

@login_required
@user_passes_test(superuser_required)
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin_order_detail.html', {'order': order})

@login_required
def customer_orders(request):
    """View for displaying a list of customer's orders."""
    # Fetch the user's orders
    orders = Order.objects.filter(user=request.user).order_by('-date_ordered')

    return render(request, 'customer_orders.html', {'orders': orders})

@login_required
def cancel_order(request, order_id):
    """Allow users to cancel orders."""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    user=request.user
    if user.is_superuser:
        if request.method == 'POST':
            order.status = 'Cancelled'
            order.save()
            return HttpResponseRedirect(reverse('order_list'))
        return render(request, 'cancel_order.html', {'order': order})
    else:
        if order.status == 'Pending':  # Only allow canceling if the order is not processed yet
            order.status = 'Cancelled'
            order.save()
            messages.success(request, "Your order has been cancelled.")
        else:
            messages.error(request, "You cannot cancel this order.")

    return redirect('customer_orders')

@login_required
@user_passes_test(superuser_required)
def order_list(request):
    orders = Order.objects.all().order_by('-date_ordered')  # List all orders, sorted by latest
    return render(request, 'order_list.html', {'orders': orders})

@login_required
@user_passes_test(superuser_required)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')  # Retrieve new status from the form
        if new_status in dict(Order.STATUS_CHOICES):  # Validate status
            order.status = new_status
            order.save()
            return HttpResponseRedirect(reverse('admin_order_detail', args=[order.id]))
    
    return render(request, 'update_status.html', {'order': order, 'statuses': Order.STATUS_CHOICES})

@login_required
@user_passes_test(superuser_required)
def mark_as_paid(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        order.is_paid = True
        order.save()
        return HttpResponseRedirect(reverse('admin_order_detail', args=[order.id]))
    
    return render(request, 'mark_as_paid.html', {'order': order})