from fabric.api import env, local, run, task, sudo, put, get, cd
from fabric.contrib.project import upload_project, rsync_project
from fabric.contrib import files
from fabtools.vagrant import vagrant
from fabtools.python import virtualenv
import fabtools

import os

env.webapps_path = '/webapps'
env.project_name = 'fuzzyfurry'
env.project_root = os.path.join(env.webapps_path, env.project_name)
env.log_path = os.path.join(env.project_root, 'log')
#env.virtualenv_path = os.path.join(env.webapps_path, env.project_name)
#env.requirements_path = os.path.join(env.webapps_path, env.project_name, 'requirements')

@task
def install_system_requirements():
    sudo('apt-get update')
    sudo('apt-get install -y'
            ' rsync'
            #' authbind'
            ' gcc'
            ' python-dev'
            ' python-virtualenv'
            #' virtualenvwrapper'
            ' nginx'
            ' supervisor'
            )
    #run('sudo apt-get install python-pip')

@task
def setup_system():
    group_name = 'www-data'
    #sudo('groupadd %s' % group)
    if not fabtools.group.exists(group_name):
        fabtools.group.create(group_name)

    #fabtools.user.create('gunicorn',
    #        system=False,
    #        create_home=False,
    #        group='www-data',
    #        shell='/usr/bin/bash',
    #        )

    #fabtools.user.modify(env.user, extra_groups=group_name)
    sudo('usermod -a -G %s %s' % (group_name, env.user))

    #sudo('mkdir -p %s' % env.webapps_path)
    #sudo('chmod 0755 %s' % env.webapps_path)

    sudo('mkdir -p %s' % env.project_root)
    sudo('chmod 775 %s' % env.project_root)
    sudo('chown %s:%s %s' % (env.user, group_name, env.project_root))


    run('mkdir -p %s' % env.log_path)
    sudo('chmod 775 %s' % env.log_path)
    sudo('chown %s:%s %s' % (env.user, group_name, env.log_path))

    sudo('mkdir -p %s' % '/webapps/log')
    sudo('chmod 775 %s' % '/webapps/log')
    sudo('chown %s:%s %s' % (env.user, group_name, '/webapps/log'))

    run('mkdir -p %s' % '/webapps/fuzzyfurry/run')
    sudo('chmod 775 %s' % '/webapps/fuzzyfurry/run')
    sudo('chown %s:%s %s' % (env.user, group_name, '/webapps/fuzzyfurry/run'))

@task
def setup_virtualenv():
    run('virtualenv -p /usr/bin/python2.7 %s' % env.project_root)

@task
def install_development_requirements():
    with cd(env.project_root):
        with virtualenv('.'):
            run('pip install -r requirements/development.txt')

@task
def deploy_nginx():
    # TODO should nginx be under supervisor?
    #sudo('mkdir -p %s' % '/var/log/nginx')
    #sudo('chown www-data:www-data %s' % '/var/log/nginx')

    put('config/dev/nginx.conf', '/etc/nginx/conf.d/', use_sudo=True)

    #files.append('/etc/nginx/nginx.conf',
    #        'daemon off;', use_sudo=True)

    #files.sed('/etc/nginx/nginx.conf',
    #        'access_log .*',
    #        'access_log %s;' % os.path.join(env.project_root, 'log', 'access.log'),
    #        backup='',
    #        use_sudo=True)
    #files.sed('/etc/nginx/nginx.conf',
    #        'error_log .*',
    #        'error_log %s;' % os.path.join(env.project_root, 'log', 'error.log'),
    #        backup='',
    #        use_sudo=True)
@task
def deploy_supervisor():
    put('config/dev/supervisor.conf', '/etc/supervisor/conf.d/', use_sudo=True)
    sudo('chmod 755 %s' % '/etc/supervisor/conf.d/supervisor.conf')
    #fabtools.service.restart('supervisor')

@task
def create_development_environment():
    install_system_requirements()
    setup_system()

    deploy_project()

    setup_virtualenv()
    install_development_requirements()

    deploy_nginx()
    fabtools.service.start('nginx')

    deploy_supervisor()
    fabtools.supervisor.reload_config()

@task
def start_development_environment():
    start_nginx()
    start_supervisor()
    # Started by supervisor
    #start_gunicorn()

#service supervisord start/reload
#supervisorctl {start,status,stop}
@task
def start_supervisor():
    if not fabtools.service.is_running('supervisor'):
        fabtools.service.start('supervisor')

@task
def start_nginx():
    #fabtools.supervisor.start_process('nginx')
    if not fabtools.service.is_running('nginx'):
        fabtools.service.start('nginx')
    #run('supervisor nginx start')

@task
def start_gunicorn():
    fabtools.supervisor.start_process('gunicorn')
    #run('supervisor fuzzyfurry_gunicorn start')

@task
def deploy_static():
    with cd(env.project_root):
        run('./manage.py collectstatic -v0 --noinput')

@task
def deploy_project():
    rsync_project(remote_dir=env.webapps_path)
    sudo('chown :%s %s' % ('www-data', '/webapps/fuzzyfurry/scripts/start_gunicorn.sh'))

@task
def deploy():
    # migrate
    # update
    #upload_project(local_dir=None, remote_dir='')
    deploy_project()
    deploy_static()


@task
def uname():
    run('uname -a')
