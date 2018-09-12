# Fennec sync tests

To run these tests you will need [Python 2][] and [pipenv][] installed. You will also
need a Fennec build running on your device along with Robocop:

```
$ cd /path/to/mozilla-central
$ mach build
$ mach package
$ mach install
$ mach robocop --serve
```

Then, to run the tests:

```
$ cd /path/to/fennec-sync-tests
$ pipenv install
$ pipenv run pytest --app org.mozilla.fennec
```

[Python 2]: http://docs.python-guide.org/en/latest/starting/installation/#legacy-python-2-installation-guides
[pipenv]: http://docs.python-guide.org/en/latest/dev/virtualenvs/#installing-pipenv
