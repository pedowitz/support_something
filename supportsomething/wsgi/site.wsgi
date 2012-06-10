import sys

activate_this = '/home/ubuntu/workspace/support_something/env/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

source_this = '/home/ubuntu/workspace/settings.py'
execfile(source_this, dict(__file__=source_this))

sys.path.insert(0, '/home/ubuntu/workspace/support_something')

from supportsomething import app as application