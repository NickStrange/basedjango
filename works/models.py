from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime


class Work(models.Model):

    CATEGORY_CHOICES = [
        ('Painting', 'Painting'),
        ('Drawing', 'Drawing'),
        ('Photography', 'Photography'),
        ('Sketch Pad', 'Sketch Pad'),
        ('Electromedia', 'Electromedia'),
        ('Videograms', 'Videograms'),
        ('Poetry Poster', 'Poetry Poster'),
        ('Notebook', 'Notebook'),
        ('Album', 'Album'),
    ]

    SOURCE_CHOICES = [
        ('Aldo foundation', 'Aldo foundation'),
        ('Anna', 'Anna'),
        ('Gifted', 'Gifted'),
    ]

    item_id = models.CharField(max_length=16, unique=True)
    source = models.CharField(max_length=16, null=False, blank=False, choices=SOURCE_CHOICES, default='Aldo foundation')
    notes = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    inventory_date = models.DateField(null=True, blank=True, default=datetime.now())
    title = models.TextField(null=True, blank=True)
    series = models.TextField(null=True, blank=True)
    # type
    date_year = models.TextField(null=True, blank=True)
    medium = models.TextField(null=True, blank=True)
    signature_and_writing = models.TextField(null=True, blank=True)
    condition = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=16, null=True, blank=True, choices=CATEGORY_CHOICES, default='Painting')
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    depth = models.FloatField(null=True, blank=True)
    size_note = models.TextField(null=True, blank=True)
    # dimensions
    file1 = models.CharField(max_length=32, null=True, blank=True)
    file2 = models.CharField(max_length=32, null=True, blank=True)
    file3 = models.CharField(max_length=32, null=True, blank=True)
    file4 = models.CharField(max_length=32, null=True, blank=True)
    file5 = models.CharField(max_length=32, null=True, blank=True)
    # url1
    # url2
    # url3
    # url4
    # url5W

    def __str__(self):
        return f"Work(item_id='{self.item_id}',title='{self.title}')"
