from django import forms
from .models import StockEntry, Bean

class StockEntryForm(forms.ModelForm):
    
    class Meta:
        model = StockEntry
        fields = [
            "bean",
            "qty_added",
            "qty_used"
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
            "origin",
            "supplier",
            "notes",
            "reorder_trigger",
            "reorder_qty"
        ]
        widgets = {
            'notes': forms.Textarea(attrs={'placeholder':'Notes'})
        }