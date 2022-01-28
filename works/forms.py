from django import forms
from works.models import Work
from django.contrib.admin import widgets


class WorkLoadForm(forms.Form):
    file_name = forms.FileField(max_length=100)

class DateInput(forms.DateInput):
    input_type = 'date'

class WorkDDLForm(forms.ModelForm):

    class Meta:
        model = Work
        fields = ['id',
                  'item_id',
                  'category',
                  'source',
                  'inventory_date',
                  'notes',
                  'location',
                  'value',
                  'title',
                  'series',
                  'date_year',
                  'medium',
                  'signature_and_writing',
                  'condition',
                  'height',
                  'width',
                  'depth',
                  'size_note',
                  'file1',
                  'file2',
                  'file3',
                  'file4',
                  'file5']

class WorkForm (forms.Form):
    class Meta:
        model = Work
        fields = ['id',
                  'item_id',
                  'category',
                  'source',
                  'inventory_date',
                  'notes',
                  'location',
                  'value',
                  'title',
                  'series',
                  'date_year',
                  'medium',
                  'signatures_and_writing',
                  'condition',
                  'height',
                  'width',
                  'depth',
                  'size_note',
                  'file1',
                  'file2',
                  'file3',
                  'file4',
                  'file5']


class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=20, label='')
