import os
from flask import Flask
import models

app = Flask('supportsomething')
app.config.from_object('supportsomething.settings')
app.config.from_envvar('SETTINGS', silent=True)

# Init models
models.init(app)

# Import modules
import views
    
    
