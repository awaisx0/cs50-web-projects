from django import forms

class NewPageForm(forms.Form):
    title = forms.CharField(max_length=64)
    content = forms.CharField(widget=forms.Textarea)
    
class EditPageForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)