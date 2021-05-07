from django.db import models


class ModelWithCodeName(models.Model):
    code = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Country(ModelWithCodeName):
    continent = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'


class City(ModelWithCodeName):
    country_code = models.CharField(max_length=10)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name="cities")

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Airport(ModelWithCodeName):
    country_code = models.CharField(max_length=5)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, related_name="airports")
    city_code = models.CharField(max_length=5)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name="airports")
    type_code = models.CharField(max_length=2, null=True, blank=True)

    class Meta:
        verbose_name = 'Аэропорт'
        verbose_name_plural = 'Аэропорты'
