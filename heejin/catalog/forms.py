from django import forms
from .models import Product

class AddClientForm(forms.Form):
    client_names_file = forms.FileField()

class AddResinForm(forms.Form):
    resin_file = forms.FileField()

class AddProductForm(forms.Form):
    product_file = forms.FileField()
    


