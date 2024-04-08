from asgi_cors import asgi_cors
from datasette import hookimpl


@hookimpl
def asgi_wrapper(datasette):
    config = datasette.plugin_config("datasette-cors") or {}
    allow_all = config.get("allow_all") or False
    hosts = config.get("hosts") or []
    host_wildcards = config.get("host_wildcards") or []
    headers = config.get("headers") or []
    methods = config.get("methods") or []
    max_age = config.get("max_age")

    def wrap_with_asgi_cors(app):
        if not (hosts or host_wildcards or allow_all or headers or methods or max_age):
            return app

        return asgi_cors(
            app,
            allow_all=allow_all,
            hosts=hosts,
            host_wildcards=host_wildcards,
            headers=headers,
            methods=methods,
            max_age=max_age,
        )

    return wrap_with_asgi_cors
