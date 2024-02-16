from django import forms
from .models import StockEntry

class StockEntryForm(forms.ModelForm):
    
    class Meta:
        model = StockEntry
        fields = ("bean","qty_added","qty_used",)