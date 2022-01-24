from django.db import models

sort_field = 'first_name'


# Create your models here.
class Contact(models.Model):
    title = models.CharField(max_length=6, null=True, blank=True)
    first_name = models.CharField(max_length=24, null=True, blank=True)
    last_name = models.CharField(max_length=24, null=True, blank=True)
    phone_number = models.CharField(max_length=24, null=True, blank=True)
    email_address = models.CharField(max_length=24, null=True, blank=True)
    company_name = models.CharField(max_length=24, null=True, blank=True)
    address = models.CharField(max_length=24, null=True, blank=True)
    city = models.CharField(max_length=24, null=True, blank=True)
    country = models.CharField(max_length=24, null=True, blank=True)
    state = models.CharField(max_length=24, null=True, blank=True)
    post_code = models.CharField(max_length=24, null=True, blank=True)

    def __str__(self):
        return f"{self.title}. {self.first_name} {self.last_name}"
