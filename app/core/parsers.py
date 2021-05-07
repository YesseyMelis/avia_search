import urllib3
import xmltodict
from django.conf import settings
import logging

from django.core.management.color import no_style
from django.db import transaction, connection

from app.core.models import Country, City, Airport

logger = logging.getLogger(__name__)


def get_countries():
    """ Get and update countries """
    url = settings.WSTRANS["COUNTRIES_URL"]
    http = urllib3.PoolManager()
    print("Getting countries.")
    response = http.request('GET', url)

    try:
        data = xmltodict.parse(response.data)
        countries = data['Countries']['Country']
        countries_length = len(countries)
        if countries_length == 0:
            logger.warning("Incorrect countries size. Len: {}. Response: {}".format(countries_length, str(countries)))
            raise Exception("Incorrect countries size. Len: {}. Response: {}".format(countries_length, str(countries)))

        with transaction.atomic():
            country_ids = list(Country.objects.all().values_list('id', flat=True))

            sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Country])
            cursor = connection.cursor()
            for sql in sequence_sql:
                cursor.execute(sql)

            for item in countries:
                country, created = Country.objects.update_or_create(
                    code=item.get('CountryCode'),
                    defaults={
                        'name': item.get('CountryName'),
                        'continent': item.get('Continent')
                    },
                )
                try:
                    country_ids.remove(country.id)
                except ValueError:
                    pass
            print('Finished saving countries.')
    except Exception as ex:
        logger.error('Countries xml parse error: {}'.format(ex))


def get_cities():
    """ Get and update cities """
    url = settings.WSTRANS["CITIES_URL"]
    http = urllib3.PoolManager()
    print("Getting cities.")
    response = http.request('GET', url)

    try:
        data = xmltodict.parse(response.data)
        cities = data['Cities']['City']
        cities_length = len(cities)
        if cities_length == 0:
            logger.warning("Incorrect cities size. Len: {}. Response: {}".format(cities_length, str(cities)))
            raise Exception("Incorrect cities size. Len: {}. Response: {}".format(cities_length, str(cities)))

        with transaction.atomic():
            city_ids = list(City.objects.all().values_list('id', flat=True))

            sequence_sql = connection.ops.sequence_reset_sql(no_style(), [City])
            cursor = connection.cursor()
            for sql in sequence_sql:
                cursor.execute(sql)

            for item in cities:
                country = Country.objects.filter(code=item.get('CountryCode')).first()
                city, created = City.objects.update_or_create(
                    code=item.get('CityCode'),
                    defaults={
                        'name': item.get('CityName'),
                        'country_code': item.get('CountryCode'),
                        'country': country if country else None
                    },
                )
                try:
                    city_ids.remove(city.id)
                except ValueError:
                    pass
            print('Finished saving cities.')
    except Exception as ex:
        logger.error('Cities xml parse error: {}'.format(ex))


def get_airports():
    """ Get and update airports """
    url = settings.WSTRANS["AIRPORTS_URL"]
    http = urllib3.PoolManager()
    print("Getting airports.")
    response = http.request('GET', url)

    try:
        data = xmltodict.parse(response.data)
        airports = data['Airports']['Airport']
        airports_length = len(airports)
        if airports_length == 0:
            logger.warning("Incorrect airports size. Len: {}. Response: {}".format(airports_length, str(airports)))
            raise Exception("Incorrect airports size. Len: {}. Response: {}".format(airports_length, str(airports)))

        with transaction.atomic():
            airport_ids = list(Airport.objects.all().values_list('id', flat=True))

            sequence_sql = connection.ops.sequence_reset_sql(no_style(), [Airport])
            cursor = connection.cursor()
            for sql in sequence_sql:
                cursor.execute(sql)

            for item in airports:
                country = Country.objects.filter(code=item.get('CountryCode')).first()
                city = City.objects.filter(code=item.get('CityCode')).first()
                airport, created = Airport.objects.update_or_create(
                    code=item.get('AirportCode'),
                    defaults={
                        'name': item.get('AirportName'),
                        'country_code': item.get('CountryCode'),
                        'country': country if country else None,
                        'city_code': item.get('CityCode'),
                        'city': city if city else None,
                        'type_code': item.get('TypeCode')
                    },
                )
                try:
                    airport_ids.remove(airport.id)
                except ValueError:
                    pass
            print('Finished saving airports.')
    except Exception as ex:
        logger.error('Airports xml parse error: {}'.format(ex))


def get_core_data():
    get_countries()
    get_cities()
    get_airports()
