# encoding: UTF-8

import shutil
import requests
import json as _json


class LoggingSession(requests.Session):
    '''
    Extend requests.Session to log requests and responses.
    '''

    def __init__(self, verbose=False, auth=None, **kwargs):
        '''
        Extend constructor with new arguments:
        - verbose: if True, print requests and responses
        '''
        self.verbose = verbose
        self.term_width = shutil.get_terminal_size((80, 20))[0]
        super(LoggingSession, self).__init__(**kwargs)
        self.auth = auth

    def prepare_request(self, request):
        '''
        Log request:
        - request: request to log
        '''
        request = super(LoggingSession, self).prepare_request(request)
        if self.verbose:
            print('='*self.term_width)
            print('> {0} {1}'.format(request.method, request.url))
            headers = request.headers if request.headers else []
            for key in sorted(headers):
                print('> {key}: {value}'.format(key=key, value=headers[key]))
            if request.body:
                try:
                    body = _json.loads(request.body.decode('UTF-8') if \
                           isinstance(request.body, bytes) else request.body)
                    print(format(_json.dumps(body, sort_keys=True, indent=4,
                                             separators=(',', ': '))))
                except _json.JSONDecodeError:
                    print(request.body)
        return request

    def request(self, **kwargs): #pylint: disable=arguments-differ
        '''
        Log requests responses:
        - kwargs: arguments passed to parent request() method
        '''
        response = super(LoggingSession, self).request(**kwargs)
        if self.verbose:
            print('-'*self.term_width)
            if isinstance(response, requests.Response):
                print('< http {status_code} {reason}'.format(status_code=response.status_code,
                                                             reason=response.reason))
                for key in sorted(response.headers.keys()):
                    print('< {key}: {value}'.format(key=key, value=response.headers[key]))
                content_type = response.headers['content-type'] \
                               if 'content-type' in response.headers else ''
                if content_type.startswith('application/json'):
                    if response.content:
                        source = response.json()
                        print(format(_json.dumps(source, sort_keys=True, indent=4,
                                                 separators=(',', ': '))))
            else:
                print('Returned:', response)
        return response


class BadStatusCodeException(Exception):
    '''
    Exception that is raised when a response doesn't have expected status code.
    '''

    def __init__(self, expected, actual, message):
        self.expected = expected
        self.actual = actual
        self.message = message
        super().__init__('Bad status code (expected: %d, actual: %d): %s' % \
                         (self.expected, self.actual, self.message[:200]))


class DjangoRestClient:

    def __init__(self, url, username, password, verbose=False):
        self.url = url
        self.session = LoggingSession(verbose, auth=(username, password))

    def request(self, url, method='GET', status=200, json=None, params=None, headers=None):
        '''
        Perform an API call:
        - url: The last part of URL, such as 'settings/modules'.
        - method: The HTTP method, defaults to GET.
        - status: expected response status code, defaults to 200.
        - json: data to send in the body as Json.
        - params: URL parameters as a dictionnary.
        '''
        if headers is None:
            headers = {}
        self.session.headers.update(headers)
        response = self.session.request(url=self.url+url, method=method, headers=headers,
                                        json=json, params=params)
        if response.status_code != status:
            raise BadStatusCodeException(expected=status, actual=response.status_code,
                                         message=response.text)
        # DEBUG
        print('>>>', response.text)
        return response.json()
