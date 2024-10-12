from django.db import models
from django.contrib.auth.models import User
from Cart.models import Order
import uuid  # for generating unique invoice numbers

class Payment(models.Model):
    STATUS_CHOICES = [
        ('SUCCESS', 'Success'),
        ('FAILED', 'Failed'),
        ('PENDING', 'Pending'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True)
    razorpay_signature = models.CharField(max_length=100, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment for Order {self.order.id} - {self.get_status_display()}"


class Invoice(models.Model):
    invoice_number = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    issued_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.invoice_number}"

    @property
    def invoice_filename(self):
        return f"invoice_{self.invoice_number}.pdf"