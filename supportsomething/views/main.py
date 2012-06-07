from flask import Module, render_template, request, session, g

main = Module(__name__)

@main.route('/')
def index():
    return render_template('index.html')