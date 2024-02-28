<!--
@since 2024.02.21, 16:15
@changed 2024.02.21, 16:15
-->

# dds-invoicing-app

The DDS invoicing app.

- Version: 0.0.4
- Last changes timestamp: 2024.02.29 00:20 +0700

TODO: Add the project description.

## See also

- [CHANGELOG](CHANGELOG.md)
- [TODO](TODO.md)

- [Sources workflow](src/README.md)

## Project resources

Repository: https://github.com/lilliputten/dds-invoicing-app

Demo deploy server: dds-invoicing-server.lilliputten.ru

Demo deploy client (TODO)): dds-invoicing-client.lilliputten.ru

## Related resources

DDS Logo & style guidelines: https://github.com/Depart-de-Sentier/dds-logo

## Server

Server runs on python/flask platform.

TODO: Describe basic server functionality.

To check django version:

```
$ python -m django --version
```

To install django:

```
python -m pip install Django
```

Used django version: 5.0.2

To run local dev server, use (for example, on 8080 port):

```
python manage.py runserver 8080
```

To migrate data:

```
python manage.py migrate
```

Create user:

```
python manage.py createsuperuser
```

## Python venv maintenance

Server command for creating venv:

```
virtualenv -p python3 ~/.venv-py3.10-flask
source ~/.venv-py3.10-flask/bin/activate
pip install -r requirements.txt
```

Local script for venv creating and initialization:

```
sh utils/util-venv-init.sh
```

Local command for activate venv:

```
call .venv/Scripts/activate
source .venv/Scripts/activate
```


## Python dependencies

```
pip install PKGNAME
pip install -r requirements-general.txt -r requirements-dev-only.txt
pip freeze > requirements-frozen.txt
```

Use `utils/venv-init.*` scripts.


