# HelloBirdie — Project Notes

## Backend test command

pytest is configured via `backend/pytest.ini` and `backend/conftest.py`.
Run the backend suite from `backend/` with no env vars needed:

```bash
cd backend
python -m pytest
```

How it works:

- `pytest.ini` sets `DJANGO_SETTINGS_MODULE = hellobirdie.settings` (the package)
- `conftest.py` sets `DJANGO_ENV=test` via `os.environ.setdefault`, so the
  settings dispatch in `hellobirdie/settings/__init__.py` loads `test.py`
- To override (e.g., run against local settings): `DJANGO_ENV=local python -m pytest`

`manage.py test` also works for quick runs against local settings:

```bash
python manage.py test api.tests.<test_module>
```

## Python version

Managed via pyenv. Project version pinned in `.python-version` (currently 3.13.15).
