from django import forms

class AddClientForm(forms.Form):
    client_names_file = forms.FileField()

    


