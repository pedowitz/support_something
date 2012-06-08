from flask import url_for, session, redirect, request
from flaskext.oauth import OAuth
from supportsomething import app

oauth = OAuth()

facebook = oauth.remote_app('facebook',
                            base_url='https://graph.facebook.com/',
                            request_token_url=None,
                            access_token_url='/oauth/access_token',
                            authorize_url='https://www.facebook.com/dialog/oauth'
                            ,
                            consumer_key=app.config['FACEBOOK_APP_ID'],
                            consumer_secret=app.config['FACEBOOK_APP_SECRET'],
                            request_token_params={'scope': 'email'}
)


@app.route('/login')
def login():
    return facebook.authorize(callback=url_for('facebook_authorized',
                                               next=url_for('upload'),
                                               _external=True))


@app.route('/login/authorized')
@facebook.authorized_handler
def facebook_authorized(resp):
    if resp is None:
        return 'Access denied: reason=%s error=%s' % (
            request.args['error_reason'],
            request.args['error_description']
            )
    session['oauth_token'] = (resp['access_token'], '')
    me = facebook.get('/me')
    app.logger.debug(me.data)
    app.logger.debug('Logged in as id=%s name=%s redirect=%s' %\
           (me.data['id'], me.data['name'], request.args.get('next')))
    return redirect(request.args.get('next'))


@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')