MAIN_URL = "http://localhost:53028/"
GAIN = 1
TOTALLY_DRY = 1650
TOTALLY_WET = 640
SOIL_WILTING_POINT = 1055


def _get_field_capacity_from_web():
    try:
        import requests
        r = requests.get(url=MAIN_URL + "sensor?action=get_field_capacity")
        print(r)
        data = r.json()
        print(data)
        return data['field_capacity']
    except requests.exceptions.ConnectionError as e:
        print(e)
    except requests.exceptions.HTTPError as e:
        print(e)
    except requests.exceptions.Timeout as e:
        print(e)
    except requests.exceptions.TooManyRedirects as e:
        print(e)
    except requests.exceptions.RequestException as e:
        print(e)


def get_field_capacity():
    try:
        import redis
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        if r.exists('field_capacity'):
            return int(r.get('field_capacity'))
        else:
            return _get_field_capacity_from_web()
    except ModuleNotFoundError:
        return _get_field_capacity_from_web()


SOIL_FIELD_CAPACITY = get_field_capacity()
print(SOIL_FIELD_CAPACITY)
GPIO_POS = 26
DRY = 0
WET = 100
URL = MAIN_URL + "sensor_status_reporter"

