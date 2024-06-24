# django-healthy

[![PyPI - Version](https://img.shields.io/pypi/v/django-healthy.svg)](https://pypi.org/project/django-healthy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/django-healthy.svg)](https://pypi.org/project/django-healthy)


-----

**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

First, install the `django-healthy` package:

```console
pip install django-healthy
```

In your `settings.py`, configure `HEALTH_CHECK_BACKENDS` with your desired indicators.

```python
HEALTH_CHECK_BACKENDS = {
    "cache": {
        "BACKEND": "healthy.backends.CacheHealthBackend",
    },
    "db": {
        "BACKEND": "healthy.backends.DatabasePingBackend",
    },
}
```

Lastly, add `django-healthy`'s routes to your `urls.py`:

```python
path("", include("healthy.urls")),
```

This adds two routes:
* `/ping/`
* `/health/`

## License

`django-healthy` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
