# Community PlanIt Documentation #
Community PlanIt is a community engagement platform maintained by Emerson College's [Engagement Game Lab](http://engagementgamelab.org/ "Engagement Game Lab").

# Development Environment Setup #
This project is using Django 1.4, Python 2.7, PostgreSQL. 

## VirtualEnv ##
We recommend using [virtualenv](http://www.virtualenv.org/en/latest/index.html "Virtual Env") to create an isolated Python environment for development.

## Dependencies via Buildout and Pip ##
Dependencies and server configurations are available via [buildout](http://www.buildout.org/ "Buildout") and/or [pip](http://pypi.python.org/pypi/pip/ "pip"). The corresponding buildout recipe and requirements.txt are available under the /config/ folder.

### Buildout ###
    python bootstrap.py
    ln -s config/buildout.cfg.local buildout.cfg
    buildout

### Pip ###
`pip install -r config/requirements.txt`

## Database Setup ##

## Initial Data ##

## Server Configuration ##

# Multilingual #
Community PlanIt supports multilingual translations using [django locale urls](http://packages.python.org/django-localeurl/) and [django-nani](http://readthedocs.org/docs/django-nani/en/0.0.3/index.html). 