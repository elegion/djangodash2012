import factory
import requests

class ResponseF(factory.Factory):
    FACTORY_FOR = requests.Response

    status_code = 200
    headers = {}
    url = 'http://example.com/'
    content = 'Example content'

    @classmethod
    def _prepare(cls, create, **kwargs):
        r = requests.Response()
        kwargs['_content'] = kwargs.pop('content')
        for attr, value in kwargs.iteritems():
            setattr(r, attr, value)
        return r
