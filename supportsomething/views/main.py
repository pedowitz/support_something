from dateutil import parser as date_parser
from boto.s3.connection import S3Connection
from flask import url_for, session, redirect, request, render_template
from flaskext.oauth import OAuth
from supportsomething import app
from uuid import uuid4


facebook = OAuth().remote_app('facebook',
                              base_url='https://graph.facebook.com/',
                              request_token_url=None,
                              access_token_url='/oauth/access_token',
                              authorize_url='https://www.facebook.com/dialog/oauth'
                              ,
                              consumer_key=app.config['FACEBOOK_APP_ID'],
                              consumer_secret=app.config['FACEBOOK_APP_SECRET'],
                              request_token_params={'scope': 'email'}
)

conn = S3Connection(aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                    aws_secret_access_key=app.config[
                                          'AWS_SECRET_ACCESS_KEY'])
bucket = conn.get_bucket('support-something')

@app.route('/')
def index():
    imgs = []
    for key in bucket.list('imgs'):
        if key.name != 'imgs/':
            imgs.append((
                'https://support-something.s3.amazonaws.com/%s' % key.name,
                date_parser.parse(key.last_modified)))

    imgs = sorted(imgs, key=lambda img: img[1], reverse=True)

    fb = None
    latitude = None
    longitude = None
    if facebook:
        try:
            fb = True
            location_id = facebook.get('/me').data['location']['id']
            location = facebook.get('/%s' % location_id).data
            latitude = location['location']['latitude']
            longitude = location['location']['longitude']
        except Exception:
            fb = False
            print 'no token yet'

    return render_template('index.html', imgs=imgs, fb=fb, latitude=latitude,
                           longitude=longitude)


@app.route('/upload')
def upload():
    return render_template('upload.html')


@app.route('/upload_image', methods=['POST'])
def upload_image():
    file = request.files['file']
    app.logger.debug(file)
    url = ''
    if file:
        url = _upload_to_s3(file)
    return url


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


def _upload_to_s3(file):
    key_name = '%s/%s-%s' % (
        'imgs', str(uuid4()),
        file.filename.replace(' ', '_').encode('ascii', 'ignore'))
    key = bucket.get_key(key_name)
    if not key:
        key = bucket.new_key(key_name)
        key.set_metadata('Content-Type', file.content_type)
        key.set_contents_from_file(file, reduced_redundancy=True)
        key.make_public()
    return key.generate_url(expires_in=60 * 30 * 12, query_auth=False)
