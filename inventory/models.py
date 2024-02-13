from django.db import models

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
    qty_total = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self) -> str:
        return f"{self.date} {self.bean.name} ({self.qty_added}, {self.qty_used}, {self.qty_total})"
    
    class Meta:
        verbose_name = "Stock Entry"
        verbose_name_plural = "Stock Entries"
