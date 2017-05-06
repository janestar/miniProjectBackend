from django import forms
class bottleForm(forms.Form):
    action = forms.CharField()
    uid = forms.CharField()
    bottleId = forms.CharField()
    bottleStatus = forms.CharField()