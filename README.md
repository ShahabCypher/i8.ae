<div align="center">
 <br />
 <p>
  <a href="https://i8.ae"><img src="https://discord.com/assets/7c13aa0def6ccb6932f47dedd33f59c1.svg" width="150" alt="i8.ae" /></a>
 </p>
</div>

# i8.ae Python Library
<br>

## Table of contents
- [About](#about)
- [Installation](#installation)
- [API key](#api-key)
- [Example Usage](#example-usage)
- [Error handling](#error-handling)
- [Rate limit](#rate-limit)
- [Links](#links)

## About
- Python client for the [i8.ae](https://i8.ae/) URL shortener — [API docs](https://i8.ae/developers)
- advantages
  - FREE to use
  - password-protect links
  - every field the API documents (`custom`, `expiry`, `domain`, `campaign`, `deeplink`, …) passed straight through
  - typed exceptions, connection pooling, configurable timeout

## Installation
```
pip install i8.ae
```
Requires Python 3.9+.

## API key
- You have to first login to [i8.ae](https://i8.ae/) then go to [developers page](https://i8.ae/developers) and copy your API key

## Example Usage
```py
from i8_ae import i8

client = i8("YOUR_API_KEY")

# link shortener
short = client.short("https://github.com/")
print(short)  # Output: https://i8.ae/ETyxT

# link shortener (with password)
short = client.short("https://github.com/", "pass")
print(short)  # Output: https://i8.ae/WSRdf

# any other documented field is forwarded as-is
short = client.short(
    "https://github.com/",
    custom="github",
    expiry="2030-01-01 00:00:00",
)
print(short)  # Output: https://i8.ae/github

# request timeout in seconds (default 10)
client = i8("YOUR_API_KEY", timeout=30)
```

## Error handling
```py
from time import sleep
from i8_ae import i8, I8Error, AuthError, RateLimitError, RequestError, APIError

client = i8("YOUR_API_KEY")

try:
    short = client.short("https://github.com/")
except RateLimitError as e:
    print("throttled, retry after header:", e.reset)
except AuthError:
    print("bad or expired API key")
except I8Error as e:
    print(e, "status:", e.status, "error code:", e.error)
```

| Exception | Raised when |
| --- | --- |
| `AuthError` | HTTP 401 / 403 — missing, invalid or expired key |
| `RateLimitError` | HTTP 429 — carries `.reset` (`X-RateLimit-Reset` header) |
| `RequestError` | timeout, DNS, TLS or connection failure |
| `APIError` | API returned `error != 0`, a non-JSON body, or a payload without `shorturl` |
| `I8Error` | base class — catches all of the above |

## Rate limit
The API allows 30 requests per minute. On HTTP 429 a `RateLimitError` is raised and `.reset` holds the `X-RateLimit-Reset` response header.

## Links
- [PyPI](https://pypi.org/project/i8.ae)
- [API docs](https://i8.ae/developers)
- [About me](https://github.com/ShahabCypher)
