from django.db import models
from django.utils import timezone

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
    contact_date = models.DateField(null=True, blank=True, default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.title:
            self.title = None
        if not self.first_name:
            self.first_name = None
        if not self.last_name:
            self.last_name = None
        if not self.phone_number:
            self.phone_number = None
        if not self.email_address:
            self.email_address = None
        if not self.company_name:
            self.company_name = None
        if not self.address:
            self.address = None
        if not self.city:
            self.city = None
        if not self.country:
            self.country = None
        if not self.state:
            self.country = None
        if not self.post_code:
            self.post_code = None
        print ("DATE", self.contact_date, "____")
        if not self.contact_date:
            self.contact_date = timezone.now()
        super(Contact, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.title}. {self.first_name} {self.last_name}"
