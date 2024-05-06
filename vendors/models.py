from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils import timezone
from django.db.models import Avg, ExpressionWrapper, F, DurationField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError

User = get_user_model()

class vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    vendor_code = models.CharField(max_length=20, unique=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating_avg = models.FloatField(default=0)
    average_response_time = models.FloatField(default=0)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return self.name
    




class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True, primary_key=True)
    vendor = models.ForeignKey(vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(default=timezone.now)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number

    def get_absolute_url(self):
        return reverse('purchase_order_detail', args=[str(self.id)])

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} historical performance on {self.date}"

    def get_absolute_url(self):
        return reverse('historical_performance_detail', args=[str(self.id)])
    

@receiver(post_save, sender=PurchaseOrder)
def update_on_time_delivery_rate(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        on_time_deliveries = completed_pos.filter(delivery_date__lte=instance.delivery_date).count()
        total_completed_pos = completed_pos.count()
        if total_completed_pos > 0:
            vendor.on_time_delivery_rate = (on_time_deliveries / total_completed_pos) * 100
            vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_quality_rating_avg(sender, instance, created, **kwargs):
    if instance.quality_rating is not None:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed')
        quality_ratings = completed_pos.exclude(quality_rating=None).aggregate(avg_quality_rating=Avg('quality_rating'))
        vendor.quality_rating_avg = quality_ratings['avg_quality_rating']
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_average_response_time(sender, instance, created, **kwargs):
    if instance.acknowledgment_date is not None:
        vendor = instance.vendor
        completed_pos = PurchaseOrder.objects.filter(vendor=vendor, status='completed', acknowledgment_date__isnull=False)
        response_times = completed_pos.annotate(response_time=ExpressionWrapper(F('acknowledgment_date') - F('issue_date'), output_field=DurationField())).aggregate(avg_response_time=Avg('response_time'))
        vendor.response_time_avg = response_times['avg_response_time']
        vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def update_fulfillment_rate(sender, instance, created, **kwargs):
    vendor = instance.vendor
    all_pos = PurchaseOrder.objects.filter(vendor=vendor)
    fulfilled_pos = all_pos.filter(status='completed', quality_rating__isnull=False)
    fulfillment_rate = (fulfilled_pos.count() / all_pos.count()) * 100
    vendor.fulfillment_rate = fulfillment_rate
    vendor.save()

@receiver(post_save, sender=PurchaseOrder)
def handle_missing_data(sender, instance, created, **kwargs):
    if instance.status == 'completed':
        if instance.delivery_date is None or instance.issue_date is None:
            raise ValidationError("Delivery date or issue date cannot be empty for completed purchase orders.")

        if instance.status == 'completed' and instance.quality_rating is None:
            raise ValidationError("Quality rating cannot be empty for completed purchase orders.")