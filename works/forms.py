from django import forms
from works.models import Work


class WorkLoadForm(forms.Form):
    file_name = forms.FileField(max_length=100)


class WorkDDLForm(forms.ModelForm):

    class Meta:
        model = Work
        fields = ['id',
                  'item_id',
                  'source',
                  'notes',
                  'location',
                  'value',
                  'inventory_date',
                  'title',
                  'series',
                  'date_year',
                  'medium',
                  'signature_and_writing',
                  'condition',
                  'category',
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
                  'source',
                  'notes',
                  'location',
                  'value',
                  'inventory_date',
                  'title',
                  'series',
                  'date_year',
                  'medium',
                  'signatures_and_writing',
                  'condition',
                  'category',
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
    search_text = forms.CharField(max_length=10, label='')
