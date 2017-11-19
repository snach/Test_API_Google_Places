import os
import requests
from tests import utils


class TestKey:

    def setup_class(self):
        self.KEY = os.getenv('KEY')
        if self.KEY is None:
            print('need export KEY=<your API_KEY>')
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
        utils.check_request_status(r, 'INVALID_REQUEST')

    def test_smoke(self):
        r = requests.get(self.BASE_URL + "?location=-33.8670522,151.1957362&radius=1&key=" + self.KEY)
        utils.check_request_status_OK(r)


class TestLocation:

    def setup_class(self):
        self.KEY = os.getenv('KEY')
        if self.KEY is None:
            print ('need export KEY=<your API_KEY>')
            exit()
        self.BASE_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?radius=500&key=' + self.KEY

    def test_without_location(self):
        r = requests.get(self.BASE_URL)
        utils.check_request_status(r, 'INVALID_REQUEST')

    def test_zero_location(self):
        r = requests.get(self.BASE_URL + '&location=0,0')
        utils.check_request_status(r, 'ZERO_RESULTS')

    def test_limit_values(self):
        # location=a,b , where a=[-90,90], b=[-180,180]

        for latitude in ('-90', '90'):                          # right latitude, wrong longitude
            for longitude in ('-180.1', '180.1'):
                r = requests.get(self.BASE_URL + '&location=' + latitude + ',' + longitude)
                utils.check_request_status(r, 'INVALID_REQUEST')

        for latitude in ('-90.1', '90.1'):                       # wrong latitude, right longitude
            for longitude in ('-180', '180'):
                r = requests.get(self.BASE_URL + '&location=' + latitude + ',' + longitude)
                utils.check_request_status(r, 'INVALID_REQUEST')

        for latitude in ('-90', '90'):                           # right latitude, right longitude
            for longitude in ('-180', '180'):
                r = requests.get(self.BASE_URL + '&location=' + latitude + ',' + longitude)
                utils.check_request_status_OK(r)

    def test_long_value(self):
        long_value = '9' * 1000
        r = requests.get(self.BASE_URL + '&location=-89.' + long_value + ',-179.' + long_value)
        utils.check_request_status_OK(r)

    def test_int_value(self):
        r = requests.get(self.BASE_URL + '&location=55,38')
        utils.check_request_status_OK(r)

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
        utils.check_request_status(r, 'INVALID_REQUEST')

    def test_bad_radius(self):
        r = requests.get(self.BASE_URL + "&radius=0")
        utils.check_request_status(r, 'INVALID_REQUEST')
        r = requests.get(self.BASE_URL + "&radius=-100")
        utils.check_request_status(r, 'INVALID_REQUEST')

    def test_more_radius_more_places(self):
        r = requests.get(self.BASE_URL + "&radius=1")
        r_json_small = utils.check_request_status_OK(r)
        qty_places_small_radius = len(r_json_small.get('results'))

        r = requests.get(self.BASE_URL + "&radius=100")
        r_json_big = utils.check_request_status_OK(r)
        qty_places_big_radius = len(r_json_big.get('results'))

        assert (qty_places_small_radius < qty_places_big_radius)

        names_small = dict()
        for i in range(len(r_json_small.get('results'))):
            names_small[r_json_small.get('results')[i].get('name')] = 1
        names_big = dict()
        for i in range(len(r_json_big.get('results'))):
            names_big[r_json_big.get('results')[i].get('name')] = 1

        for key in names_small.keys():
            assert (key in names_big)