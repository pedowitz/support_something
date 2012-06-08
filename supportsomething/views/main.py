from boto.s3.connection import S3Connection
from flask import render_template, request
from supportsomething import app
from uuid import uuid4

conn = S3Connection(aws_access_key_id=app.config['AWS_ACCESS_KEY_ID'],
                    aws_secret_access_key=app.config[
                                          'AWS_SECRET_ACCESS_KEY'])
bucket = conn.get_bucket('support-something')

@app.route('/')
def index():
    imgs = []
    for key in bucket.list('imgs'):
        if key.name != 'imgs/':
            print key.name
            imgs.append('https://support-something.s3.amazonaws.com/%s' % key.name)

    return render_template('index.html', imgs=imgs)


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
