#!/bin/bash

# Clean up all processes
killall python
killall supervisorctl
killall supervisord
killall nginx
killall gunicorn
killall memcached
killall sass

# Copy correct config files
cp /etc/supervisord.conf.planit /etc/supervisord.conf

# Launch processes
echo "here"
supervisord
echo "there"
sass --watch /home/tim/bocoup/work/git/community-planit/assets/scss:/home/tim/bocoup/work/git/community-planit/assets/css &
echo "everywhere"

# cd
cd /home/tim/bocoup/work/git/community-planit/

# Choo Choo!!!!
sl
