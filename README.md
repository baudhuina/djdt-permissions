# Permission panel for Django Debug Toolbar 

<!--- 
![License](https://img.shields.io/pypi/l/django-clearcache)
![Django versions](https://img.shields.io/pypi/djversions/django-clearcache)
![Python versions](https://img.shields.io/pypi/pyversions/django-clearcache)
-->

A simple DjDT panel displaying the permissions of the current user and their source. 

CHANGE IMAGE
![demo](https://raw.githubusercontent.com/timonweb/django-clearcache/master/demo.gif)

## Installation (on top of Django Debug Toolbar)

0. Install `django-debug-toolbar` (instructions [here](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html))


1. Install permission panel using PIP:

      ```
      pip install COMPLETE (GET FROM REPO)
      ```
<!---
      ```
      pip install djdt-permissions
      ```
-->

2. Add **djdt_permissions** to INSTALLED_APPS, make sure it's below `django.toolbaar`:

   Please note that ust as the Debug Toolbar, this panel is not supposed to be installed if 'DEBUG' is False.

      ```
      if DEBUG == True:
         INSTALLED_APPS += [
          ...
          'debug_toolbar',
          'djdt_permissions',
          ...
         ]
      ```

3. Register the new panel by adding path **djdt_permissions.panels.PermissionsPanel** 
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
<!--- Currently no migrations 
   4. Apply migrations:

   ```
   manage.py migrate [--database=<your_database>] [--settings=<your_settings>]
   ```
-->
## Usage

TO BE COMPLETED 


## Installing the test project

Would you wish to modify/contribute to this project:
1. Fork the GIT repo from Github. It contains a Django test project
2. Install dependencies: `poetry install`
3. Apply migrations: `manage.py migrate`
4. Run server: `manage.py runserver`
5. Point your browser at http://localhost:8000

To run the test:
TO BE COMPLETED

## Contact me

alain.baudhuin@skynet.be   MAKE LINK
