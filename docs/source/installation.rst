############
Installation
############


************
Requirements
************

* `Django`_ 1.4 or higher
* Python 2.7 or a higher 


************
CommunityPlanIt.org Installation Guide
************

=======================================

Installing Dependencies Using zc.buildout
-----------------------------------------

Install virtualenvwrapper and zc.buildout::

    pip install virtualenvwrapper
    pip install zc.buildout

add env variables to .bashrc::

    export WORKON_HOME=/var/local/venv
    source /usr/local/bin/virtualenvwrapper.sh

create the virtual environment::

    mkvirtualenv cpi --no-site-packages
    workon cpi

clone the repo::

    cd $VIRTUAL_ENV
    git clone git@github.com:psychotechnik/Community-PlanIt.git

initialize buildout::

    wget http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py
    bin/python bootstrap.py --distribute

    cp Community-PlanIt/config/buildout.cfg.local buildout.cfg

edit the buildout.cfg to include directories on your local workstation::

relevant options > 
    download_cache_dir
    venv_dir

[server]  > host, venv_name, etc.

run the buildout command to install dependencies and build config files::

    bin/buildout -vvN

Commands to manage the project
------------------------------
useful aliases to manage the uwsgi workers

alias runcpi='sudo su root -c "$VIRTUAL_ENV/bin/uwsgi --xml=$VIRTUAL_ENV/cpi/parts/uwsgi/uwsgi.xml &"'

alias cpib='sudo kill -HUP `cat $VIRTUAL_ENV/var/run/cpi.pid`'

alias stopcpi='sudo kill -INT `cat $VIRTUAL_ENV/var/run/uwsgi/cpi.pid`'

requires the multitail package
alias tailcpi='multitail $VIRTUAL_ENV/cpi/log/cpi.log $VIRTUAL_ENV/cpi/log/uwsgi.log'


References
----------
    http://www.doughellmann.com/docs/virtualenvwrapper/
    http://www.buildout.org/install.html




.. _Django: http://www.djangoproject.com
