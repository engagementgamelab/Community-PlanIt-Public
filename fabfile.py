from fabric.api import *

# globals 
config.project-name = 'Community PlanIt'

staging = 'www-data@dev.communityplanit.org'
production = 'wwww-data@communityplanit.org'

# Environments
def staging():
    """ Use staging server settings"""
    config.user = 'www-data'
    config.hosts = ['dev.communityplanit.org']
    config.path = '/var/local/venv/cpi/Community-PlanIt/'

def production():
    """ Use production server settings"""
    env.hosts = [production]

def all():
    """ Use all servers """
    env.hosts = [staging, production]


# Tasks
def deploy():
    """
    Deploy the latest version of the site to the servers, install any
    required third party modules, collect static files, reset caches, 
    and restart the webserver
    """
    gitpull():
    restart_memcached()
    restart_webserver()

# Helpers

def update_requirements():
    """ Install the required packages from pip requirements file"""
    
def restart_webserver():
    """ Restart the web server """

def restart_memcached():
    """ Restart the memcached server """
    sudo('service memcached restart')
    
def restart_nginx():
    sudo('service nginx restart')

def gitpull():
    """ Updates the repository """
    require("hosts", provided_by=[staging, production])
    run('cd $(path); git pull')
    
    