from django.db import models
from orders.models import OrderItem
from users.models import User


class ReturnRequest(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    order_item = models.ForeignKey(
        OrderItem,
        on_delete=models.PROTECT,
        related_name='return_requests'
    )

    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='return_requests'
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    admin_note = models.TextField(blank=True)

    requested_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Return Request #{self.id} - {self.status}"