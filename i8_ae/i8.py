import requests

BASE_URL = 'https://i8.ae'


class I8Error(Exception):
    def __init__(self, message, error=None, status=None):
        super().__init__(message)
        self.error = error
        self.status = status


class AuthError(I8Error):
    pass


class RateLimitError(I8Error):
    def __init__(self, message, reset=None, **kwargs):
        super().__init__(message, **kwargs)
        self.reset = reset


class RequestError(I8Error):
    pass


class APIError(I8Error):
    pass


class i8():
    def __init__(self, api_key, timeout=10):
        if not api_key:
            raise ValueError('api_key is required: i8("YOUR_API_KEY")')

        self.key = str(api_key).strip()
        self.timeout = timeout
        # one shared Session (connection reuse). requests.Session is not
        # documented thread-safe; if cookie-less GETs race, switch to threading.local.
        self.session = requests.Session()

        token = self.key
        if not token.lower().startswith('bearer '):
            token = 'Bearer ' + token
        self.session.headers['Authorization'] = token

    def short(self, url, password=None, **params):
        data = {'url': url, **params}
        if password is not None:
            data['password'] = password

        try:
            res = self.session.post(
                BASE_URL + '/api/url/add',
                json=data,
                timeout=self.timeout,
            )
        except requests.RequestException as exc:
            raise RequestError(str(exc)) from exc

        if res.status_code in (401, 403):
            raise AuthError(res.text[:200] or 'invalid API key', status=res.status_code)

        if res.status_code == 429:
            raise RateLimitError(
                res.text[:200] or 'rate limited',
                reset=res.headers.get('X-RateLimit-Reset'),
                status=429,
            )

        try:
            body = res.json()
        except ValueError:
            raise APIError(
                'HTTP %s: %s' % (res.status_code, res.text[:200]),
                status=res.status_code,
            )

        shorted = body.get('shorturl')
        if not res.ok or body.get('error', 0) != 0 or not shorted:
            raise APIError(
                body.get('message') or res.text[:200],
                error=body.get('error'),
                status=res.status_code,
            )

        return shorted
