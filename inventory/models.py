from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Bean(models.Model):
    name = models.CharField(max_length=50)
    origin = models.CharField(max_length=50, blank=True)
    supplier = models.CharField(max_length=50, blank=True)
    notes = models.CharField(max_length=500, blank=True)
    reorder_trigger = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reorder_qty = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # override string representation for developing purposes
    def __str__(self) -> str:
        return f"{self.name}"

class StockEntry(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=True) # auto_now_add set to true for creation date
    bean = models.ForeignKey("Bean", on_delete=models.CASCADE)
    qty_added = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    qty_used = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.date} {self.bean.name} ({self.qty_added}, {self.qty_used})"

    class Meta:
        verbose_name = "Stock Entry"
        verbose_name_plural = "Stock Entries"
        unique_together = ('bean', 'date')

    @property
    def qty_total(self):
        return self.qty_added - (self.qty_used or 0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        update_stock_totals(self.bean)

class StockOffset(models.Model):
    bean = models.OneToOneField(Bean, on_delete=models.CASCADE, related_name='stock_offset')
    total_offset = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.bean.name} Stock Offset"

    class Meta:
        verbose_name = "Stock Offset"
        verbose_name_plural = "Stock Offsets"

class StockTotal(models.Model):
    bean = models.OneToOneField(Bean, on_delete=models.CASCADE, related_name='stock_total')
    total_quantity = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self) -> str:
        return f"{self.bean.name} Stock Total"
    
    class Meta:
        verbose_name = "Stock Total"
        verbose_name_plural = "Stock Totals"

def update_stock_totals(bean):
    # Calculate sum of qty_added and qty_used for the given bean
    total_qty_added = StockEntry.objects.filter(bean=bean).aggregate(models.Sum('qty_added'))['qty_added__sum'] or 0
    total_qty_used = StockEntry.objects.filter(bean=bean).aggregate(models.Sum('qty_used'))['qty_used__sum'] or 0

    # Calculate total quantity taking into account the stock offset value
    total_quantity = total_qty_added - total_qty_used + bean.stock_offset.total_offset

    # Update or create the StockTotal entry for the bean
    stock_total, created = StockTotal.objects.get_or_create(bean=bean)
    stock_total.total_quantity = total_quantity
    stock_total.save()

@receiver(post_save, sender=StockEntry)
def update_stock_totals_on_stock_entry_save(sender, instance, **kwargs):
    update_stock_totals(instance.bean)

@receiver(post_save, sender=StockOffset)
def update_stock_totals_on_stock_offset_save(sender, instance, **kwargs):
    update_stock_totals(instance.bean)