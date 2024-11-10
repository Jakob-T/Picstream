from django import forms
from .models import Image

# Form for uploading posts
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image', 'caption']
