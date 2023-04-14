from django import forms

class AddClientForm(forms.Form):
    client_name = forms.CharField(max_length=50)

    def clean_client_name(self):

        data = self.cleaned_data['client_name']

        return data
    


