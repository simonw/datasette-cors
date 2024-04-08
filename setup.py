from setuptools import setup
import os

VERSION = "1.0"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-cors",
    description="Datasette plugin for configuring CORS headers",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-cors",
    license="Apache License, Version 2.0",
    version=VERSION,
    py_modules=["datasette_cors"],
    entry_points={"datasette": ["cors = datasette_cors"]},
    install_requires=["asgi-cors>=1.0"],
    extras_require={"test": ["datasette", "pytest", "pytest-asyncio", "httpx"]},
    tests_require=["datasette-cors[test]"],
)
