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


def check_keys(need_keys, response_keys):  # check response_keys are equivalent need_keys

    for key in need_keys:
        assert (key in response_keys)
        delete_index = response_keys.index(key)
        del response_keys[delete_index]

    assert (len(response_keys) == 0)