from flask import Module, render_template, request, session, g

api = Module(__name__, url_prefix='/api')

@api.route('/')
def index():
    return "Index of api."