import sys
from io import BytesIO
import requests
from PIL import Image

# Пусть наше приложение предполагает запуск:
# python search.py Москва, ул. Ак. Королева, 12
# Тогда запрос к геокодеру формируется следующим образом:
toponym_to_find = " ".join(sys.argv[1:])

geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

geocoder_params = {
    "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
    "geocode": toponym_to_find,
    "format": "json"}

response = requests.get(geocoder_api_server, params=geocoder_params)

if not response:
    # обработка ошибочной ситуации
    pass

# Преобразуем ответ в json-объект
json_response = response.json()
with open('result.txt', 'w', encoding='utf-8') as f:
    print(json_response, file=f)
# Получаем первый топоним из ответа геокодера.
toponym = json_response["response"]["GeoObjectCollection"][
    "featureMember"][0]["GeoObject"]
# Координаты центра топонима:
toponym_coordinates = toponym["Point"]["pos"]
# Долгота и широта:
envelope_longitude, envelope_lattitude = toponym['boundedBy']['Envelope']['lowerCorner'].split(' ')
toponym_longitude, toponym_lattitude = toponym_coordinates.split(' ')

delta1 = str(2 * abs(float(toponym_longitude) - float(envelope_longitude)))
delta2 = str(2 * abs(float(toponym_lattitude) - float(envelope_lattitude)))

# Собираем параметры для запроса к StaticMapsAPI:
map_params = {
    "ll": ",".join([toponym_longitude, toponym_lattitude]),
    "spn": ",".join([delta1, delta2]),
    "l": "map",
    "pt": "{0},pm2dgl".format(','.join([toponym_longitude, toponym_lattitude]))
}

map_api_server = "http://static-maps.yandex.ru/1.x/"
# ... и выполняем запрос
response = requests.get(map_api_server, params=map_params)

Image.open(BytesIO(
    response.content)).show()
# Создадим картинку
# и тут же ее покажем встроенным просмотрщиком операционной системы
