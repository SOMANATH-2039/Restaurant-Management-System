from django.db import models

class Category(models.Model):
    """Category for classifying inventory items."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    """Represents an item in the inventory."""
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="items")
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.quantity} in stock"

    @property
    def total_value(self):
        """Total value of the inventory item based on quantity and price."""
        return self.quantity * self.price
