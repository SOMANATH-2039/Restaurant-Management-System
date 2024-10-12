from django.db import models
from django.contrib.auth.models import User
from Menu.models import MenuItems  
class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, blank=True, null=True)  # For anonymous users

    def __str__(self):
        return f"Cart ({self.id})"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.cart_items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.cart_items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name="cart_items", on_delete=models.CASCADE)
    product = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

    @property
    def total_price(self):
        return self.product.price * self.quantity
    
    class Meta:
        verbose_name_plural="Cart Items"

# class Order(models.Model):
#     user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
#     created_at = models.DateTimeField(auto_now_add=True)
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     is_paid = models.BooleanField(default=False)

#     def __str__(self):
#         return f"Order {self.id}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),         # Order placed but not yet processed
        ('Processing', 'Processing'),   # Order is being processed (e.g., payment is being verified)
        ('Shipped', 'Shipped'),         # Order is shipped (if applicable)
        ('Delivered', 'Delivered'),     # Order is delivered
        ('Cancelled', 'Cancelled'),     # Order was cancelled
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')  # Add the status field
    is_paid = models.BooleanField(default=False)  # To track if the order has been paid

    def __str__(self):
        return f"Order #{self.id} - {self.user.username}"

    @property
    def order_items(self):
        return self.orderitem_set.all()  # Assuming a related_name is not explicitly set


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(MenuItems, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)


    @property
    def total_price(self):
        return self.quantity * self.product.price

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"