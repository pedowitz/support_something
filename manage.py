from supportsomething import app
app.run(host=app.config.get('HOST', '127.0.0.1'), port=app.config.get('PORT', 5000))