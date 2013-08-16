#!/bin/bash
 
NAME="fuzzyfurry" # Name of the application
DJANGODIR=/webapps/fuzzyfurry # Django project directory
#SOCKFILE=/webapps/fuzzyfurry/run/gunicorn.sock # we will communicte using this unix socket
# USER=michal # the user to run as
# GROUP=michal # the group to run as
# NUM_WORKERS=3 # how many worker processes should Gunicorn spawn
# DJANGO_SETTINGS_MODULE=fuzzyfurry.settings # which settings file should Django use
 
 
echo "Starting $NAME"
 
# Activate the virtual environment
cd $DJANGODIR
source bin/activate
export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
export PYTHONPATH=$DJANGODIR:$PYTHONPATH
 
# Create the run directory if it doesn't exist
#RUNDIR=$(dirname $SOCKFILE)
#test -d $RUNDIR || mkdir -p $RUNDIR
 
# Start your Django Unicorn
exec gunicorn \
$NAME.wsgi:application \
-c $DJANGODIR/config/dev/gunicorn.py
#--name $NAME \
#--workers $NUM_WORKERS \
#--user=$USER --group=$GROUP \
#--log-level=debug \
#--bind=unix:$SOCKFILE
