from django.db import models

class Work(models.Model):

    CATEGORY_CHOICES = [
        ('PT', 'Painting'),
        ('PH', 'Photography'),
        ('SK', 'Sketch Pad'),
        ('EM', 'Electromedia'),
        ('VG', 'Videograms'),
        ('PP', 'Poetry Poster'),
        ('NB', 'Notebook'),
        ('AB', 'Album'),
    ]

    SOURCE_CHOICES = [
        ('AF', 'Aldo foundation'),
        ('A', 'Anna'),
        ('G', 'Gifted'),
    ]

    item_id = models.CharField(max_length=16, unique=True)
    source = models.CharField(max_length=2, null=True, blank=True, choices=SOURCE_CHOICES)
    notes = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    inventory_date = models.DateField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    series = models.TextField(null=True, blank=True)
    # type
    date_year = models.TextField(null=True, blank=True)
    medium = models.TextField(null=True, blank=True)
    signature_and_writing = models.TextField(null=True, blank=True)
    condition = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=2, null=True, blank=True, choices=CATEGORY_CHOICES)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    depth = models.IntegerField(null=True, blank=True)
    size_note = models.TextField(null=True, blank=True)
    #dimensions
    file1 = models.CharField(max_length=32, null=True, blank=True)
    file2 = models.CharField(max_length=32, null=True, blank=True)
    file3 = models.CharField(max_length=32, null=True, blank=True)
    file4 = models.CharField(max_length=32, null=True, blank=True)
    file5 = models.CharField(max_length=32, null=True, blank=True)
    # url1
    # url2
    # url3
    # url4
    # url5

    def __str__(self):
        return f"Work(item_id='{self.item_id}',title='{self.title}')"
