from asgi_cors import asgi_cors
from datasette import hookimpl


@hookimpl
def asgi_wrapper(datasette):
    config = datasette.plugin_config("datasette-cors") or {}
    allow_all = config.get("allow_all") or False
    hosts = config.get("hosts") or []
    host_wildcards = config.get("host_wildcards") or []

    def wrap_with_asgi_cors(app):
        if not (hosts or host_wildcards or allow_all):
            return app

        return asgi_cors(
            app,
            allow_all=allow_all,
            hosts=hosts,
            host_wildcards=host_wildcards,
        )

    return wrap_with_asgi_cors
