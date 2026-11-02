'''Flask CTS webservice.

Serve the Canonical Text Services API for a collection of TEI xml files.
Following https://github.com/Capitains/tutorial-nemo
'''

import os

import flask
from flask_nemo import Nemo
from capitains_nautilus.cts.resolver import NautilusCtsResolver
from capitains_nautilus.flask_ext import FlaskNautilus

app = flask.Flask("CTS webserver demo (nemo)")

LOCAL_CONFIG = 'config.py'
if os.path.exists(LOCAL_CONFIG):
    app.config.from_pyfile(LOCAL_CONFIG)

corpora = [entry.path for entry in os.scandir('corpora') if entry.is_dir()]
print('app: resolver given', corpora)
resolver = NautilusCtsResolver(corpora)
resolver.parse()

nautilus = FlaskNautilus(
        prefix='/api',
        app=app,
        resolver=resolver
)

nemo = Nemo(
        name='Nemo',
        app=app,
        resolver=resolver,
        base_url='/nemo'
)


@app.route('/')
def home():
    '''Placeholder home page to help visitors.

    We're mainly here to serve the nemo browser and api endoints,
    but provide a simple landing page in case we're serving the
    whole domain.'''
    return flask.render_template('index.html',
                                 nemo=nemo.prefix,
                                 nautilus=nautilus.prefix,
                                 scaife=app.config.get('SCAIFE_URL'))


if __name__ == '__main__':
    app.run(debug=True)
