import multiprocessing
import sys
import os

sys.path.append('/webapps/fuzzyfurry')

django_settings = 'fuzzyfurry.settings.dev'
#bind = '127.0.0.1:8000'
bind = 'unix:/webapps/fuzzyfurry/run/gunicorn.sock'
workers = multiprocessing.cpu_count() * 2 + 1
log_level = 'debug'
log_file = '/webapps/fuzzyfurry/log/gunicorn.log'

