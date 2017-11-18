import pytest
import os
import requests
#from utils import utils

def check_request_status_OK(request):
        assert (request.status_code == 200)
        r_json = request.json()
        assert (r_json.get('status') == "OK")
        assert (len(r_json.get('results')) != 0)
        return r_json


def check_request_status(request, status):  # don't use for status OK
        assert (request.status_code == 200)
        r_json = request.json()
        assert (r_json.get('status') == status)
        assert (len(r_json.get('results')) == 0)

class TestKey:

    def setup_class(self):
        self.KEY = os.getenv('KEY')
        if self.KEY is None:
            print ('need export KEY=<your API_KEY>')
            exit()
        self.BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

    def test_without_key(self):
        r = requests.get(self.BASE_URL)
        assert (r.status_code == 200)
        r_json = r.json()
        assert (r_json.get('error_message') == 'This service requires an API key.')
        assert (r_json.get('status') == 'REQUEST_DENIED')

    def test_bad_key(self):
        r = requests.get(self.BASE_URL + "?key=12345678JFFD")
        assert (r.status_code == 200)
        r_json = r.json()
        assert (r_json.get('error_message') == 'The provided API key is invalid.')
        assert (r_json.get('status') == 'REQUEST_DENIED')

    def test_only_key(self):
        r = requests.get(self.BASE_URL + "?key=" + self.KEY)
        check_request_status(r, 'INVALID_REQUEST')

    def test_smoke(self):
        r = requests.get(self.BASE_URL + "?location=-33.8670522,151.1957362&radius=1&key=" + self.KEY)
        check_request_status_OK(r)


class TestLocation:

    def setup_class(self):
        self.KEY = os.getenv('KEY')
        if self.KEY is None:
            print ('need export KEY=<your API_KEY>')
            exit()
        self.BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius=500&key=' + self.KEY

    def test_without_location(self):
        r = requests.get(self.BASE_URL)
        check_request_status(r, 'INVALID_REQUEST')

    def test_zero_location(self):
        r = requests.get(self.BASE_URL + '&location=0,0')
        check_request_status(r, 'ZERO_RESULTS')

    def test_limit_values(self):
        # location=a,b , where a=[-90,90], b=[-180,180]

        for latitude in ('-90', '90'):                          # right latitude, wrong longitude
            for longitude in ('-180.1', '180.1'):
                r = requests.get(self.BASE_URL + '&location=' + latitude + ',' + longitude)
                check_request_status(r, 'INVALID_REQUEST')

        for latitude in ('-90.1', '90.1'):                       # wrong latitude, right longitude
            for longitude in ('-180', '180'):
                r = requests.get(self.BASE_URL + '&location=' + latitude + ',' + longitude)
                check_request_status(r, 'INVALID_REQUEST')

        for latitude in ('-90', '90'):                           # right latitude, right longitude
            for longitude in ('-180', '180'):
                r = requests.get(self.BASE_URL + '&location=' + latitude + ',' + longitude)
                check_request_status_OK(r)

    def test_long_value(self):
        long_value = '9' * 1000
        r = requests.get(self.BASE_URL + '&location=-89.' + long_value + ',-179.' + long_value)
        check_request_status_OK(r)

    def test_int_value(self):
        r = requests.get(self.BASE_URL + '&location=55,38')
        check_request_status_OK(r)

class TestRadius:

    def setup_class(self):
        self.KEY = os.getenv('KEY')
        if self.KEY is None:
            print ('need export KEY=<your API_KEY>')
            exit()
        self.BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?' \
                        '&key=' + self.KEY + \
                        '&location=55.797208,37.5355793'      # location Mail.Ru

    def test_without_radius(self):
        r = requests.get(self.BASE_URL)
        check_request_status(r, 'INVALID_REQUEST')

    def test_bad_radius(self):
        r = requests.get(self.BASE_URL + "&radius=0")
        check_request_status(r, 'INVALID_REQUEST')
        r = requests.get(self.BASE_URL + "&radius=-100")
        check_request_status(r, 'INVALID_REQUEST')

    def test_more_radius_more_places(self):
        r = requests.get(self.BASE_URL + "&radius=1")
        r_json = check_request_status_OK(r)
        qty_places_small_radius = len(r_json.get('results'))

        r = requests.get(self.BASE_URL + "&radius=100")
        r_json = check_request_status_OK(r)
        qty_places_big_radius = len(r_json.get('results'))

        assert (qty_places_small_radius < qty_places_big_radius)




























