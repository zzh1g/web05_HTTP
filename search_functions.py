from io import BytesIO
import requests
from PIL import Image


def show_image(toponym_longitude, toponym_lattitude, delta):
    map_params = {
        "ll": ",".join([toponym_longitude, toponym_lattitude]),
        "spn": ",".join([delta[0], delta[1]]),
        "l": "map",
        "pt": "{0},pm2dgl".format(','.join([toponym_longitude, toponym_lattitude]))
    }
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_api_server, params=map_params)
    Image.open(BytesIO(
        response.content)).show()


def get_delt(data):
    toponym_to_find = " ".join(data)
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": toponym_to_find,
        "format": "json"}
    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass
    json_response = response.json()
    #with open('result.txt', 'w', encoding='utf-8') as f:
    #    print(json_response, file=f)
    toponym = json_response["response"]["GeoObjectCollection"][
        "featureMember"][0]["GeoObject"]
    toponym_coordinates = toponym["Point"]["pos"]
    envelope_longitude, envelope_lattitude = toponym['boundedBy']['Envelope']['lowerCorner'].split(' ')
    toponym_longitude, toponym_lattitude = toponym_coordinates.split(' ')
    delta1 = str(2 * abs(float(toponym_longitude) - float(envelope_longitude)))
    delta2 = str(2 * abs(float(toponym_lattitude) - float(envelope_lattitude)))
    delta = (delta1, delta2)
    show_image(toponym_longitude, toponym_lattitude, delta)
