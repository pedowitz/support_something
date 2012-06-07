import os
from flask import Flask
import settings
import models

def create_app(environment=None):
    app = Flask('supportsomething')

    # Config app for environment
    if not environment:
        environment = os.environ.get('SUPPORTSOMETHING_ENVIRONMENT', 'Dev')

    app.config.from_object('supportsomething.settings.%s' % environment)

    # Init models
    models.init(app)

    # Import modules
    
    from supportsomething.views.api import api
    
    from supportsomething.views.main import main
    
    
    # Register modules with app
    
    app.register_module(api)
    
    app.register_module(main)
    
    
    return app