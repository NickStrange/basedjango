from django import forms
from original.models import OldWork


class WorkLoadForm(forms.Form):
    file_name = forms.FileField(max_length=100)


class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=20, label='')


class OldWorkForm (forms.Form):
    class Meta:
        model = OldWork
        fields = ['index',
                  'item_id',
                  'source',
                  'notes',
                  'location',
                  'value',
                  'inventory_date',
                  'title',
                  'series',
                  'type',
                  'date_year',
                  'medium',
                  'signature_and_writing',
                  'condition',
                  'category',
                  'height',
                  'width',
                  'depth',
                  'size_note',
                  'dimensions',
                  'file1',
                  'file2',
                  'file3',
                  'file4',
                  'file5',
                  'url1',
                  'url2',
                  'url3',
                  'url4',
                  'url5']
