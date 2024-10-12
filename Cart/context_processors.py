from .models import Cart

def cart_context(request):
    """Make the cart accessible globally to all templates."""
    cart = None
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
    else:
        session_key = request.session.session_key
        if not session_key:
            request.session.create()  # Create session if it doesn't exist
        cart = Cart.objects.filter(session_key=request.session.session_key).first()

    # Calculate total items and total price
    total_items = cart.total_items if cart else 0
    total_price = cart.total_price if cart else 0

    return {
        'cart': cart,
        'cart_total_items': total_items,
        'cart_total_price': total_price,
    }
