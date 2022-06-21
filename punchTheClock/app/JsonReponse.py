from django.http import JsonResponse

from django.core.serializers.json import DjangoJSONEncoder


class PTCJsonResponse(JsonResponse):
    def __init__(self, message, data=None, object=None, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs):
        if not data:
            data = {}
        data['message'] = message
        if object:
            data['object'] = object
        super().__init__(data, encoder, safe, json_dumps_params, **kwargs)


class PTCJsonResponseForbidden(PTCJsonResponse):
    def __init__(self, message='Forbidden', data=None, object=None, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs):
        super().__init__(message, data, object, encoder, safe, json_dumps_params, **kwargs)
        self.status_code = 403


class PTCJsonResponseNotAllowed(PTCJsonResponse):
    def __init__(self, message='Not allowed', data=None, object=None, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs):
        super().__init__(message, data, object, encoder, safe, json_dumps_params, **kwargs)
        self.status_code = 405


class PTCJsonResponseServerError(PTCJsonResponse):
    def __init__(self, message='Server error', data=None, object=None, encoder=DjangoJSONEncoder, safe=True, json_dumps_params=None, **kwargs):
        super().__init__(message, data, object, encoder, safe, json_dumps_params, **kwargs)
        self.status_code = 500
