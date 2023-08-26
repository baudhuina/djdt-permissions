# Permission panel for Django Debug Toolbar 

![License](https://img.shields.io/pypi/l/djdt-permissions)
![Django versions](https://img.shields.io/pypi/djversions/djdt-permissions)
![Python versions](https://img.shields.io/pypi/pyversions/djdt-permissions)

A simple DjDT panel displaying the permissions granted to the current user, how the 
current user obtained each one of them (directly or through a group 
membership), and the resulting consolidated permissions set.

<img width="500" alt="djdt-permission_capture" src="https://github.com/baudhuina/djdt-permissions/assets/26870372/b936a1a1-b9f7-48c8-a9ee-a9c9f77c6989">

## Installation (on top of Django Debug Toolbar)

First, install `django-debug-toolbar` (instructions 
<a href='https://django-debug-toolbar.readthedocs.io/en/latest/installation.html' target='_blank'>here</a>), then:


1. Install permission panel, either with Pip or Poetry:

      ```
      pip install 'git+https://github.com/baudhuina/djdt-permissions.git@1.0.0#egg=djdt_permissions'
      ```
      or complete your project's  `pyproject.toml` file with XXX TO BE COMPLETED and run `poetry install` or `poetry update`.

    <!---
          ```
          pip install djdt-permissions
          ```
    -->

2. Add `djdt_permission` to `INSTALLED_APPS`, make sure it's below `django.toolbar`:

   Please note that just as the Debug Toolbar, this panel is not supposed to be installed if 'DEBUG' is False.

      ```
      if DEBUG == True:
         INSTALLED_APPS += [
          ...
          'debug_toolbar',
          'djdt_permissions',
          ...
         ]
      ```

3. Register the new panel by adding path `djdt_permissions.panels.PermissionsPanel` 
 to setting `DEBUG_TOOLBAR_PANELS` (which is entirely conditional to `DEBUG`). The 
 sequence of the panels defines their order in the toolbar.

   ```
   DEBUG_TOOLBAR_PANELS = [
        'djdt_permissions.panels.PermissionsPanel',
        'debug_toolbar.panels.history.HistoryPanel',
        'debug_toolbar.panels.versions.VersionsPanel',
        # ... any other panel.
    ]
   ```
   
4. (optional) If you want the panel to be disabled by default, add its full path
    in the `DEBUG_TOOLBAR_CONFIG[DISABLE_PANELS]` set.

    ```
    DEBUG_TOOLBAR_CONFIG = {
        "DISABLE_PANELS":  {
             'djdt_permissions.panels.permissions_panelPermissionsPanel',
             # any other panel to disable
         },
        # other config settings.
    ]
    ```

<!--- Currently no migrations 
   5. Apply migrations:

   ```
   manage.py migrate [--database=<your_database>] [--settings=<your_settings>]
   ```
-->
## Usage

The Permission Panel is used just as any other panel of the Django Debug Toolbar:
- Open DJdT overlay;
- Enable, disable, consult the panel at will...


## Installing the test project

Would you wish to modify/contribute to this project:
1. Fork the GIT repo from GitHub. It contains a Django test project.
2. Install dependencies: `poetry install`.
3. Apply migrations: `manage.py migrate [--settings=test_project.settings]`.
4. Run server: `manage.py runserver [--settings=test_project.settings]`.
5. Point your browser at http://localhost:8000.

## Running the tests

Once the test project is installed (see above), run the tests with:

    ```
    manage.py test [--database=<your_database>] [--settings=<your_settings>]
    ```

## Contact me

[alain.baudhuin@skynet.be](mailto:alain.baudhuin@skynet.be)
