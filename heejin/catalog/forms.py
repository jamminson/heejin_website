from django import forms

class AddClientForm(forms.Form):
    client_names_file = forms.FileField(label='고겍사 파일', required=False)
    client_name = forms.CharField(max_length=50, label='고겍사')

class AddResinForm(forms.Form):
    resin_file = forms.FileField(label='자재 파일', required=False)
    material_type = forms.CharField(max_length=10, label='구분')
    client_name = forms.CharField(max_length=50, label='고겍사')
    resin_name = forms.CharField(max_length=50, label='품명')

class AddProductForm(forms.Form):
    product_file = forms.FileField(label='제품 파일', required=False)
    client_name = forms.CharField(max_length=50, label='고겍사')
    model = forms.CharField(max_length=10, label='모델')
    product_code = forms.CharField(max_length=50, label='품변')
    product_name = forms.CharField(max_length=50, label='품명')
    machine_tonnage = forms.CharField(max_length=10, label='사출톤')
    resin = forms.CharField(max_length=50, label='자재 품명')
    cavity = forms.CharField(max_length=50, label='Cavity')
    ct = forms.CharField(max_length=20, label='C/T')
    week_produce = forms.CharField(max_length=10, label='주간생산량')
    night_produce = forms.CharField(max_length=10, label='야간생간량')
    real_weight = forms.CharField(max_length=10, label='실중량')
    weight = forms.CharField(max_length=10, label='중량')
    


