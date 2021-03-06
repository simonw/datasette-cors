# datasette-cors

[![PyPI](https://img.shields.io/pypi/v/datasette-cors.svg)](https://pypi.org/project/datasette-cors/)
[![CircleCI](https://circleci.com/gh/simonw/datasette-cors.svg?style=svg)](https://circleci.com/gh/simonw/datasette-cors)
[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/simonw/datasette-cors/blob/master/LICENSE)

Datasette plugin for configuring CORS headers, based on https://github.com/simonw/asgi-cors

You can use this plugin to allow JavaScript running on a whitelisted set of domains to make `fetch()` calls to the JSON API provided by your Datasette instance.

## Installation

    pip install datasette-cors

## Configuration

You need to add some configuration to your Datasette `metadata.json` file for this plugin to take effect.

To whitelist specific domains, use this:

```json
{
    "plugins": {
        "datasette-cors": {
            "hosts": ["https://www.example.com"]
        }
    }
}
```

You can also whitelist patterns like this:

```json
{
    "plugins": {
        "datasette-cors": {
            "host_wildcards": ["https://*.example.com"]
        }
    }
}
```

## Testing it

To test this plugin out, run it locally by saving one of the above examples as `metadata.json` and running this:

    $ datasette --memory -m metadata.json

Now visit https://www.example.com/ in your browser, open the browser developer console and paste in the following:

```javascript
fetch("http://127.0.0.1:8001/:memory:.json?sql=select+sqlite_version%28%29").then(r => r.json()).then(console.log)
```

If the plugin is running correctly, you will see the JSON response output to the console.
