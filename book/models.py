import datetime
from decimal import Decimal

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.db import models

from user.models import User


class Book(models.Model):
    ROLE_CHOICES = (
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
    )

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=ROLE_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BookBorrow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    books = models.ManyToManyField(Book)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_deadline = models.DateTimeField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)
    is_returned = models.BooleanField(default=False)
    fine = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_fine(self):
        if not self.is_returned and self.return_deadline and self.return_deadline < timezone.now():
            overdue_days = (timezone.now() - self.return_deadline).days
            return round(overdue_days * 5)
        return 0

    def __str__(self):
        return f"{self.user.username} borrowed"


@receiver(post_save, sender=BookBorrow)
def set_return_deadline(sender, instance, created, **kwargs):
    if created and not instance.return_deadline:
        instance.return_deadline = timezone.now() + datetime.timedelta(days=14)
        instance.save()
