# Project Pantry - A new way to browse your recipe
[![Django CI](https://github.com/PichapopRo/project-pantry/actions/workflows/django.yml/badge.svg)](https://github.com/PichapopRo/project-pantry/actions/workflows/django.yml)
[![Flake8-Flak8-Docstring-Test](https://github.com/PichapopRo/project-pantry/actions/workflows/flake8-test.yml/badge.svg)](https://github.com/PichapopRo/project-pantry/actions/workflows/flake8-test.yml)
[![codecov](https://codecov.io/gh/PichapopRo/project-pantry/graph/badge.svg?token=QJ8UVLHBVG)](https://codecov.io/gh/PichapopRo/project-pantry)

This recipe application aims to help home cooks improve their experience and reduce headaches during their cooking sessions.

This app is created as a part of the [Individual Software Process](https://cpske.github.io/ISP) course at [Kasetsart University](www.ku.ac.th) in the academic year 2024.

# Installation
Please, follow [Installation Guide](./installation/installation.md)
[utils.py](webpage%2Futils.py)
# How to run
You can run the server by following these steps.

1. Activate Python virtual environment.
- For windows
```sh
cd venv/Scripts
activate
cd ../..
```
- For MacOS/Linux
```sh
source venv/bin/activate
```
2. Run the server.
```sh
python manage.py runserver
```
3. If you wish to run a CSS file, you can do so with the following command.
```sh
python manage.py runserver --insecure
```
4. If you wish to run Selenium test, you can do so with the following command.
```sh
python seleniumfiles/s_webdriver.py
```

## Project documents
All the project documents can be accessed in [Project Wiki](../../wiki/Home).
