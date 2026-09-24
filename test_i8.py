import json

import requests

from i8_ae import i8, I8Error, AuthError, RateLimitError, RequestError, APIError

API_KEY = ''  # paste your i8.ae key here to also shorten TARGETS for real

TARGETS = [
    'https://github.com/',
    'https://www.python.org/',
]


class FakeResp:
    def __init__(self, status=200, body=None, raw=None, headers=None):
        self.status_code = status
        self.ok = status < 400
        self.headers = headers or {}
        self._body = body
        self.text = raw if raw is not None else json.dumps(body or {})

    def json(self):
        if self._body is None:
            raise ValueError('no json')
        return self._body


def stub(client, resp=None, exc=None):
    def post(url, **kwargs):
        stub.url = url
        stub.kwargs = kwargs
        if exc is not None:
            raise exc
        return resp
    client.session.post = post
    return client


def raises(exc_type, fn, **expect):
    try:
        fn()
    except exc_type as e:
        for k, v in expect.items():
            assert getattr(e, k) == v, (k, getattr(e, k), v)
        return e
    raise AssertionError('expected %s' % exc_type.__name__)


OK = FakeResp(200, {'error': 0, 'id': 1, 'shorturl': 'https://i8.ae/x'})

# Bearer prefix, request shape, return value
c = stub(i8('SECRET'), OK)
assert c.short('https://github.com/') == 'https://i8.ae/x'
assert c.session.headers['Authorization'] == 'Bearer SECRET'
assert stub.url == 'https://i8.ae/api/url/add'
assert stub.kwargs['json'] == {'url': 'https://github.com/'}
assert stub.kwargs['timeout'] == 10

# no double prefix
c = stub(i8('Bearer SECRET'), OK)
c.short('https://github.com/')
assert c.session.headers['Authorization'] == 'Bearer SECRET'

# custom timeout
c = stub(i8('k', timeout=3), OK)
c.short('https://github.com/')
assert stub.kwargs['timeout'] == 3

# password + **params passthrough
c = stub(i8('k'), OK)
c.short('https://github.com/', 'p', custom='gh', expiry='2030-01-01 00:00:00')
assert stub.kwargs['json'] == {
    'url': 'https://github.com/',
    'custom': 'gh',
    'expiry': '2030-01-01 00:00:00',
    'password': 'p',
}

# missing key fails at construction, before any request
raises(ValueError, lambda: i8(''))
raises(ValueError, lambda: i8(None))

# transport failure (requests wraps these under RequestException)
c = stub(i8('k'), exc=requests.exceptions.ConnectionError('boom'))
raises(RequestError, lambda: c.short('https://github.com/'))

# 401 / 403
c = stub(i8('k'), FakeResp(401, None, raw='unauthorized'))
raises(AuthError, lambda: c.short('https://github.com/'), status=401)

# 429 exposes rate limit reset
c = stub(i8('k'), FakeResp(429, None, raw='slow down', headers={'X-RateLimit-Reset': '1700000000'}))
raises(RateLimitError, lambda: c.short('https://github.com/'), status=429, reset='1700000000')

# API-reported error
c = stub(i8('k'), FakeResp(200, {'error': 1, 'message': 'bad url'}))
raises(APIError, lambda: c.short('https://github.com/'), error=1, status=200)

# error 0 but no shorturl in payload
c = stub(i8('k'), FakeResp(200, {'error': 0}))
raises(APIError, lambda: c.short('https://github.com/'), status=200)

# non-JSON body
c = stub(i8('k'), FakeResp(502, None, raw='<html>gateway</html>'))
raises(APIError, lambda: c.short('https://github.com/'), status=502)

# exceptions are catchable as the documented base
c = stub(i8('k'), FakeResp(401, None, raw='x'))
raises(I8Error, lambda: c.short('https://github.com/'))

print('offline ok')

created = []
if API_KEY:
    client = i8(API_KEY)
    for target in TARGETS:
        short = client.short(target)
        created.append((target, short))
        print('%s -> %s' % (target, short))

    print('created %d url(s):' % len(created))
    for target, short in created:
        print('  %s  %s' % (short, target))
else:
    print('live skipped: set API_KEY in test_i8.py to shorten TARGETS for real')
