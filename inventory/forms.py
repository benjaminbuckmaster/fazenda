from django import forms
from .models import StockEntry, Bean, StockAdjustment

class StockEntryForm(forms.ModelForm):
    
    class Meta:
        model = StockEntry
        fields = [
            "bean",
            "qty_added",
            "qty_used",
            ]
        widgets = {
            'qty_added': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
            'qty_used': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
        }

class BeanDetailsForm(forms.ModelForm):

    class Meta:
        model = Bean
        fields = [
            "name",
            "supplier",
            "cost",
            "notes",
            "reorder_trigger",
            "reorder_qty",
            "is_hidden",
            "is_ordered"
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'placeholder':'Notes'})
        }

class StockAdjustmentForm(forms.ModelForm):

    class Meta:
        model = StockAdjustment
        fields = [
            "bean",
            "adj_amount",
            ]
        widgets = {
            'adj_amount': forms.NumberInput(attrs={'placeholder': 'Enter quantity'}),
        }