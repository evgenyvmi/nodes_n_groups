from django import forms

class UploadGraphForm(forms.Form):
    graph = forms.FileField()