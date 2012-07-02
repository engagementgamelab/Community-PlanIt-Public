# Community PlanIt Documentation #
Community PlanIt is a community engagement platform for local planning efforts. Bringing together the interactivity of social networks and the incentives of online games, Community PlanIt transforms participatory planning into a fun, engaging activity for all ages. Players participate in planning-themed time-based missions to earn game coins, which they spend on the local causes most important to them. The community joins together at the end of the process to discuss the results with decision-makers and plan for the future.

This project is currently maintained by the [Engagement Game Lab](http://engagementgamelab.org/ "Engagement Game Lab") at Emerson College.

----------
# Development Environment Setup #
This project is using Django 1.4, Python 2.7, PostgreSQL. 

## VirtualEnv ##
We recommend using [virtualenv](http://www.virtualenv.org/en/latest/index.html "Virtual Env") to create an isolated Python environment for development.

## Dependencies via Buildout and Pip ##
Dependencies and server configurations are available via [buildout](http://www.buildout.org/ "Buildout") and/or [pip](http://pypi.python.org/pypi/pip/ "pip"). The corresponding buildout recipe and requirements.txt are available under the /config/ folder.

### Buildout ###
- `wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py`
- Create an `eggs` folder: `mkdir eggs`
- `mkdir log; touch log/cpi.log`
- `python bootstrap.py`
- `ln -s config/buildout.cfg.local buildout.cfg`
- `buildout [-c buildout.cfg]`

Note that the django recipe used in the buildout.cfg provides a handy binary `django` used in place of Django's default `manage.py`.

### Pip ###
- `pip install -r config/requirements.txt`

## Database Setup ##
As all content is developed in collaboration between the planner and [Engagement Game Lab](http://engagementgamelab.org/ "Engagement Game Lab"), a copy of the database is not currently available for public distribution. See the *Initial Data* section below to set up test data.

## Initial Data ##
All required initial data is provided through app fixtures (/web/*appname*/initial_data.json) and should be automatically loaded when you run `django syncdb` (or `python manage.py syncdb`). 

A set of test data will be available in the future as fixtures.
 
## Server Configuration ##

----------
# Multilingual #
Community PlanIt supports multilingual translations using [django-localeurls](http://packages.python.org/django-localeurl/) and [django-nani](http://readthedocs.org/docs/django-nani/en/0.0.3/index.html). 