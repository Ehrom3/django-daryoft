from django import forms
from .models import Item, Response

class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        fields = ['title', 'description', 'image', 'category', 'city', 'location', 'event_date', 'kind', 'status']
        widgets = {'event_date': forms.DateInput(attrs={'type': 'date'})}

