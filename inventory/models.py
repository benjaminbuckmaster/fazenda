from datetime import date
from django.db import models, transaction
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.shortcuts import render
from django.db.models import Sum


class Bean(models.Model):
    name = models.CharField(max_length=50)
    supplier = models.CharField(max_length=50, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Price per kg")
    notes = models.CharField(max_length=500, blank=True)
    reorder_trigger = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reorder_qty = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    is_hidden = models.BooleanField(default=False)
    is_ordered = models.BooleanField(default=False)

    @property
    def origin(self):
        if self.name:
            return self.name.split()[0]
        return ''

    def __str__(self) -> str:
        return f"{self.name}"
    

class StockEntry(models.Model):
    date = models.DateField(default=date.today, editable=True)
    bean = models.ForeignKey("Bean", on_delete=models.CASCADE)
    qty_added = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    qty_used = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.date} {self.bean.name} ({self.qty_added}, {self.qty_used})"

    class Meta:
        verbose_name = "Stock Adjustment"
        verbose_name_plural = "Stock Entries"
        unique_together = ('bean', 'date')

    @property
    def qty_total(self):
        return self.qty_added - (self.qty_used or 0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_stock_totals(self.bean)
    

class StockAdjustment(models.Model):
    date = models.DateField(default=date.today, editable=True)
    bean = models.ForeignKey("Bean", on_delete=models.CASCADE)
    adj_amount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.date} {self.bean.name} ({self.adj_amount})"

    class Meta:
        verbose_name = "Stock Adjustment"
        verbose_name_plural = "Stock Adjustments"
        unique_together = ('bean', 'date')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_stock_totals(self.bean)
    

class StockTotal(models.Model):
    bean = models.OneToOneField(Bean, on_delete=models.CASCADE, related_name='stock_total')
    total_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.bean.name} Stock Total"

    class Meta:
        verbose_name = "Stock Total"
        verbose_name_plural = "Stock Totals"


def update_stock_totals(bean):
    total_qty_added = StockEntry.objects.filter(bean=bean).aggregate(models.Sum('qty_added'))['qty_added__sum'] or 0
    total_qty_used = StockEntry.objects.filter(bean=bean).aggregate(models.Sum('qty_used'))['qty_used__sum'] or 0
    total_adjustment = StockAdjustment.objects.filter(bean=bean).aggregate(models.Sum('adj_amount'))['adj_amount__sum'] or 0

    total_quantity = total_qty_added - total_qty_used + total_adjustment

    with transaction.atomic():
        stock_total, created = StockTotal.objects.get_or_create(bean=bean)
        stock_total.total_quantity = total_quantity
        stock_total.save()


@receiver(post_save, sender=StockEntry)
@receiver(post_delete, sender=StockEntry)
@receiver(post_save, sender=StockAdjustment)
@receiver(post_delete, sender=StockAdjustment)
def update_stock_totals_signal(sender, instance, **kwargs):
    update_stock_totals(instance.bean)

def stock_use_over_time(request):
    # Query the stock entries and annotate with the cumulative sum
    stock_entries = (
        StockEntry.objects
        .values('date', 'bean__name')
        .annotate(qty_used=Sum('qty_used'))
        .order_by('date', 'bean__name')
    )
    
    # Format the data for the chart
    data = {}
    for entry in stock_entries:
        date = entry['date'].strftime('%Y-%m-%d')
        bean = entry['bean__name']
        qty_used = entry['qty_used']
        
        if bean not in data:
            data[bean] = []
        data[bean].append({'date': date, 'qty_used': qty_used})
    
    return render(request, 'stock_use_over_time.html', {'data': data})
