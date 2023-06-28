from django.db import models


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Address(models.Model):
    address_name = models.CharField(max_length=100)
    google_map_link = models.URLField()
    city = models.ForeignKey(City, related_name='addresses', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.city.name} {self.address_name}'

