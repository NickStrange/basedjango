from django.db import models
from django.contrib.admin.widgets import AdminDateWidget
from datetime import datetime
from django.utils import timezone


class Work(models.Model):

    CATEGORY_CHOICES = [
        ('Painting', 'Painting'),
        ('Container', 'Container'),
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
    inventory_date = models.DateField(null=True, blank=True, default=timezone.now)
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

    def gen_item_id(self):
        suffix = ''
        if self.category == 'Painting':
            suffix = 'P'
        elif self.category == 'Container':
            suffix = 'B'
        elif self.category == 'Drawing':
            suffix = 'D'
        elif self.category == 'Photography':
            suffix = 'PH'
        elif self.category == 'Sketch Pad':
            suffix = 'P'
        elif self.category == 'Electromedia':
            suffix = 'E'
        elif self.category == 'Videograms':
            suffix = 'V'
        elif self.category == 'Poetry Poster':
            suffix = 'PP'
        elif self.category == 'Notebook':
            suffix = 'N'
        elif self.category == 'Album':
            suffix = 'A'
        else:
            raise ValueError(f'Unexpected category {self.category}')
        self.item_id = f'AT.{suffix}.{self.id}'

    def save(self, *args, **kwargs):
        if not self.notes:
            self.notes = None
        if not self.location:
            self.location = None
        if not self.title:
            self.title = None
        if not self.series:
            self.series = None
        if not self.medium:
            self.medium = None
        if not self.signature_and_writing:
            self.signature_and_writing = None
        if not self.condition:
            self.condition = None
        if not self.size_note:
            self.size_note = None
        super(Work, self).save(*args, **kwargs)
        if not self.item_id:
            self.gen_item_id()
        super(Work, self).save(*args, **kwargs)

    def __str__(self):
        return f"Work(item_id='{self.item_id}',title='{self.title}')"
