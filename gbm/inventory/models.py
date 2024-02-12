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