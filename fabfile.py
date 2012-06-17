from fabric.api import *

def setup():
    '''
    To store pip downloads locally add the following to your .bashrc
    export PIP_DOWNLOAD_CACHE=~/.pip_download_cache

    In production you'll need:
    PATH=/usr/pgsql-9.0/bin:$PATH
    '''
    local('virtualenv --no-site-packages --distribute env')
    _virtualenv('pip install -r requirements.txt')


def _virtualenv(command, *args):
    result = local('. env/bin/activate&& ' + command + ' ' + ' '.join(args),
                   capture=False)
    return result

path = '/home/ubuntu/workspace/support_something'
def update_prod():
    _prod()
    with cd(path):
        run('git pull --rebase')
        run('touch supportsomething/wsgi/site.wsgi')

def run_app():
    _prod()
    with cd(path):
        run('export SETTINGS=/home/ubuntu/workspace/settings.py && . env/bin/activate&& python manage.py > ~/log &')

def _prod():
    env.host_string = 'ubuntu@ec2-23-22-24-40.compute-1.amazonaws.com'