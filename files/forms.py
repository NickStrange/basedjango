
from django import forms

class CsvForm (forms.Form):
    # class Meta:
    #     model=Csv
    #     fields=['file_name']

    file_name=forms.FileField( max_length=100)
