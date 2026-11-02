# CDLI Text Services

[![Tests](https://github.com/cdli-gh/cdli-cts-server/actions/workflows/tests.yml/badge.svg)](https://github.com/cdli-gh/cdli-cts-server/actions/workflows/tests.yml)

This repo is a webservice which provides programmatic access to
texts from the [Cuneiform Digital Library Initiative](https://cdli.ucla.edu).

It loads a set of documents laid out according to
[Capitains Guidlines](http://capitains.org/pages/guidelines)
and makes them available over the
[Canonical Text Services](http://cite-architecture.org/cts/) api.

## Quickstart

Install Python 3.13 and Git first. Run these commands from the repository root.

On Windows PowerShell, enable UTF-8 before running Python or Pipenv. The
corpus contains Unicode text, and the upstream resolver opens text files
using Python's default encoding:

```powershell
$env:PYTHONUTF8 = '1'
```

```sh
python -m pip install pipenv # If you don't already have it.
git submodule update --init  # To download the corpus collection.
```

```sh
pipenv sync --dev
pipenv run pytest
pipenv run python main.py
```

This starts a development server listening on the local machine.
It will automatically reload the server as changes to the source
are made.
From there you can
  [get available texts](http://localhost:5000/api/cts?request=GetCapabilities) or
  [fetch a text](http://localhost:5000/api/cts?request=GetPassage&urn=urn:cts:cdli:P254855.P254855.cdli-sux).
There is also a [browse interface](http://localhost:5000/nemo/).

Additional text collections can be added under `corpora`.
The server must be manually restarted afterward.

### Dependency compatibility

Use `pipenv sync --dev` to install the tested versions in `Pipfile.lock`.
The published Nautilus 1.0.3 release imports `werkzeug.contrib.cache`, which
modern Werkzeug no longer provides ([issue #13](https://github.com/cdli-gh/cdli-cts-server/issues/13)).
The Pipfile pins Nautilus to upstream commit
`cf17ffa550d207b74f4386647f4ed4be7b702ded`, which uses `cachelib` instead.
This version names its resolver `NautilusCtsResolver`.

Nemo and Nautilus still import `Markup` from Flask, so Flask must remain
below 2.3. Flask 2.2 also requires Werkzeug below 3, and both extensions
require setuptools below 81 for `pkg_resources`.
These bounds restore compatibility with the existing extensions; they do
not provide support for the current Flask and Werkzeug release lines.
Removing the bounds requires modernizing both upstream extensions first.

To check the setup after dependency changes, run:

```sh
pipenv verify
pipenv run pytest
pipenv run pycodestyle main.py test_app.py
```

## Deployment

The included `Dockerfile` can be used to deploy the server in a container.
Initialize the corpus submodule before building. The image uses Python 3.13
and installs runtime dependencies from the same lockfile as the test environment.

```sh
git submodule update --init --recursive
docker build -t cdli-cts-server .
docker run --rm -p 127.0.0.1:5048:80 cdli-cts-server
```
