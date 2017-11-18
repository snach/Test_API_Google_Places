def check_request_status_OK(request):
        assert (request.status_code == 200)
        r_json = request.json()
        assert (r_json.get('status') == "OK")
        assert (len(r_json.get('results')) != 0)


def check_request_status(request, status):  # don't use for status OK
        assert (request.status_code == 200)
        r_json = request.json()
        assert (r_json.get('status') == status)
        assert (len(r_json.get('results')) == 0)