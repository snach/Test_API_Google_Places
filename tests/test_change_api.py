import os
import requests


def check_keys(need_keys, response_keys): # check existence response_keys in need_keys

    for key in need_keys:
        assert (key in response_keys)
        delete_index = response_keys.index(key)
        del response_keys[delete_index]

    assert (len(response_keys) == 0)


class TestKeysAPI:

    def setup_class(self):
        KEY = os.getenv('KEY')
        if KEY is None:
            print('need export KEY=<your API_KEY>')
            exit()
        r = requests.get('https://maps.googleapis.com/maps/api/place/nearbysearch/json?'
                         'location=55.797208,37.5355793&radius=1&key=' + KEY)
        self.r_json = r.json()
        self.one_result = self.r_json.get('results')[0]
        # check_ok_response

    def test_first_level_including(self):
        need_keys = ('html_attributions', 'results', 'status')
        response_keys = list(self.r_json.keys())
        check_keys(need_keys, response_keys)

    def test_keys_in_results(self):
        need_keys = ('geometry', 'icon', 'id', 'name', 'photos', 'place_id', 'reference', 'scope', 'types', 'vicinity')
        response_keys = list(self.one_result.keys())
        check_keys(need_keys, response_keys)

    def test_results_geometry(self):

        need_keys_coordinates = ('lat', 'lng')

        geometry = self.one_result.get('geometry')
        need_keys_geometry = ('location', 'viewport')
        response_keys_geometry = list(geometry.keys())
        check_keys(need_keys_geometry, response_keys_geometry)

        location = geometry.get('location')
        response_keys_location = list(location.keys())
        check_keys(need_keys_coordinates, response_keys_location)

        viewport = geometry.get('viewport')
        need_keys_viewport = ('northeast', 'southwest')
        response_keys_viewport = list(viewport.keys())
        check_keys(need_keys_viewport, response_keys_viewport)

        northeast = viewport.get('northeast')
        response_keys_northeast = list(northeast.keys())
        check_keys(need_keys_coordinates, response_keys_northeast)

        southwest = viewport.get('southwest')
        response_keys_southwest = list(southwest.keys())
        check_keys(need_keys_coordinates, response_keys_southwest)

    def test_results_photos(self):
        photos = self.one_result.get('photos')[0]
        need_keys_photos = ('height', 'html_attributions', 'photo_reference', 'width')
        response_keys_photos = list(photos.keys())
        check_keys(need_keys_photos, response_keys_photos)





















