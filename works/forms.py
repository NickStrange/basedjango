from django import forms
from works.models import OldWork, Work


class WorkLoadForm (forms.Form):
    file_name=forms.FileField( max_length=100)


class OldWorkForm (forms.Form):
    class Meta:
        model=OldWork
        fields=['index',
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
                'signatures_and_writing',
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


class WorkForm (forms.Form):
    class Meta:
        model=Work
        fields=['id',
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
