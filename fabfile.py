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