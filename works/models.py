from django.db import models

# Create your models here.

class OldWork(models.Model):
    index = models.IntegerField(primary_key=True)
    item_id = models.CharField(max_length=16, unique=True)
    source = models.CharField(max_length=32, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=32, null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    inventory_date = models.DateField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    series = models.CharField(max_length=32, null=True, blank=True)
    type = models.TextField(null=True, blank=True)
    date_year = models.TextField(null=True, blank=True)
    medium = models.TextField(null=True, blank=True)
    signature_and_writing = models.TextField(null=True, blank=True)
    condition = models.TextField(null=True, blank=True)
    category = models.TextField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    depth = models.IntegerField(null=True, blank=True)
    size_note = models.TextField(null=True, blank=True)
    dimensions = models.TextField(null=True, blank=True)
    file1 = models.TextField(null=True, blank=True)
    file2 = models.TextField(null=True, blank=True)
    file3 = models.TextField(null=True, blank=True)
    file4 = models.TextField(null=True, blank=True)
    file5 = models.TextField(null=True, blank=True)
    url1 = models.TextField(null=True, blank=True)
    url2 = models.TextField(null=True, blank=True)
    url3 = models.TextField(null=True, blank=True)
    url4 = models.TextField(null=True, blank=True)
    url5 = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"OldWork(index={self.index}, item_id='{self.item_id}',title='{self.title}')"


class Work(models.Model):
    index = models.IntegerField(primary_key=True)
    item_id = models.CharField(max_length=16, unique=True)
    source = models.CharField(max_length=32, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    location = models.TextField(null=True, blank=True)
    value = models.IntegerField(null=True, blank=True)
    inventory_date = models.DateField(null=True, blank=True)
    title = models.TextField(null=True, blank=True)
    series = models.TextField(null=True, blank=True)
    date_year = models.TextField(null=True, blank=True)
    medium = models.TextField(null=True, blank=True)
    signature_and_writing = models.TextField(null=True, blank=True)
    condition = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=32,null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    depth = models.IntegerField(null=True, blank=True)
    size_note = models.TextField(null=True, blank=True)
    file1 = models.TextField(null=True, blank=True)
    file2 = models.TextField(null=True, blank=True)
    file3 = models.TextField(null=True, blank=True)
    file4 = models.TextField(null=True, blank=True)
    file5 = models.TextField(null=True, blank=True)


    def __str__(self):
        return f"Work(index={self.index}, item_id='{self.item_id}',title='{self.title}')"


