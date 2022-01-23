from .models import Contact
from django import forms

class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ['title', 'first_name', 'last_name', 'phone_number', 'email_address', 'company_name',
                  'address', 'city', 'country', 'state', 'post_code']


class UploadFileForm(forms.Form):
    file = forms.FileField()


class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=10, label='')