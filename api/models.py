from django.db import models

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=30)

    def __str__(self):
        return "{} ({})".format(self.name, self.ticker)

class Entry(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    timestamp = models.DateField()
    price = models.CharField(max_length=100)

    def __str__(self):
        return "{}@{}".format(self.company, self.timestamp)
