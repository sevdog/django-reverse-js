# Django  Reverse JS

[![Tests](https://github.com/sevdog/django-reverse-js/actions/workflows/tests.yaml/badge.svg)](https://github.com/sevdog/django-reverse-js/actions/workflows/tests.yaml)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/django-reverse-js)](https://img.shields.io/pypi/pyversions/django-reverse-js)
[![Django version](https://img.shields.io/pypi/djversions/django-reverse-js)](https://img.shields.io/pypi/djversions/django-reverse-js)


**Javascript url handling for Django that doesn’t hurt.**


_Django Reverse JS_ is a small django app that makes url handling of
[named urls](https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns) in JavaScript easy and confortable for django's users.

For example you can retrieve a named url:

```python
path('/betterliving/<str:category_slug>/<int:entry_pk>/', 'get_house', name='betterliving_get_house')
```

in JavaScript it can be resolved like:

```javascript
Urls.betterlivingGetHouse('house', 12)
// '/betterliving/house/12/'
```


# Installation

### Requirements

| Python version | Django versions    |
|----------------|--------------------|
| 3.6            | 2.2, 3.0, 3.1, 3.2 |
| 3.7            | 2.2, 3.0, 3.1, 3.2 |
| 3.8            | 2.2, 3.0, 3.1, 3.2 |
| 3.9            | 2.2, 3.0, 3.1, 3.2 |


Install using `pip`

```shell
pip install django-reverse-js
```

… or clone the project from github.

```shell
git clone https://github.com/sevdog/django-reverse-js.git
```

Add `'django_reverse_js'` to your `INSTALLED_APPS` setting.

```python
INSTALLED_APPS = (
    ...
    'django_js_reverse',
)
```

# Usage

## As a static file

First generate static file with `createstatic_reversejs` command

```shell
django-admin createstatic_reversejs
```

> NOTE: If you change some urls or add an app and want to update the reverse.js file by running again the command.

After this add the file to your template

```html
<script src="{% static 'django_reverse_js/js/reverse.js' %}"></script>
```


## As view

Include view in your _URLCONF_ (you may also cache this is needed):

```python
urlpatterns = [
    ...,
    path('reverse.js', 'django_reverse_js.views.urls_js', name='reverse_js'),
]
```

Then include JavaScript in your template

```html
<script src="{% url 'reverse_js' %}" type="text/javascript"></script>
```

## As template tag
You can place the `reverse_js` JavaScript inline into your templates,
however use of inline JavaScript is not recommended, because it
may cause problems with Content Security Policy.
See [django-csp](https://django-csp.readthedocs.io/) for further readings.

```django
{% load reversejs %}

<script type="text/javascript" charset="utf-8">
    {% reverse_js %}
</script>
```

----

## Use the resolver in JavaScript

If your url names are valid [JavaScript identifiers](https://developer.mozilla.org/en-US/docs/Glossary/Identifier)
you can access them by the _dot notation_:

```javascript
Urls.betterlivingGetHouse('house', 12)
```

If the named url contains invalid identifiers use the _square-bracket
notation_ instead:

> NOTE: ATM [_namespaced_ urls](https://docs.djangoproject.com/en/3.2/topics/http/urls/#url-namespaces) **must** be accessd in this way

```javascript
Urls['betterliving-get-house']('house', 12)
Urls['namespace:betterliving-get-house']('house', 12)
```


You can also pass javascript objects to match keyword aguments like the
examples bellow:

```javascript
Urls['betterliving-get-house']({ category_slug: 'house', entry_pk: 12 })
Urls['namespace:betterliving-get-house']({ category_slug: 'house', entry_pk: 12 })
```

# Settings

- **`REVERSEJS_VAR_NAME`**: name given to JavaScript variable used to access django urls; default `Urls`.

- **`REVERSEJS_GLOBAL_OBJECT_NAME`**: global JavaScript object to which bound resolver variable; default `window`.

- **`REVERSEJS_EXCLUDE_NAMESPACES`**: list of _url namespaces_ to be excluded from JavaScript resolver; default `[]` (aka: all namespaces allowed).

- **`REVERSEJS_INCLUDE_ONLY_NAMESPACES`**: list of _url namespaces_ to be included in JavaScript resolver; default `[]` (aka: all namespaces allowed).
  - use `''` (empty string) to allow only url without a namespace
  - use `'foo\0'` (namespace name terminated with _null-char_) to include only urls from `'foo'` namespace and prevent any inner namespace to be extracted (ie: `'foo:bar'`)

- **`REVERSEJS_SCRIPT_PREFIX`**: path of application (when served behing a reverse-proxy), needed to return full-urls; default `None`.

- **`REVERSEJS_OUTPUT_PATH`**: path where to place file created by `createstatic_reversejs` command, if not provided `STATIC_ROOT` is used; defatul `None`.

> NOTE: at the moment only one between `REVERSEJS_INCLUDE_ONLY_NAMESPACES` and `REVERSEJS_EXCLUDE_NAMESPACES` may be used.