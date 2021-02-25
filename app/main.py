'''
ContainerSSH authentication server using LDAP
'''
__author__ = 'Taavi Väänänen'
__license__ = 'BSD-3-Clause'


from logging.config import dictConfig
from flask import Flask, jsonify, request
from os import getenv
from yaml import safe_load

from ldaplookup import is_valid_key


dictConfig(
    {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            }
        },
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default',
            }
        },
        'root': {'level': 'INFO', 'handlers': ['wsgi']},
    }
)


app = Flask(__name__)


with open(getenv('CONTAINERSSH_LDAP_CONFIG', '/config.yaml')) as f:
    app.config.update(safe_load(f.read()))


@app.route('/')
def home():
    return 'ContainerSSH auth server'


@app.route('/password', methods=['GET', 'POST'])
def password():
    return jsonify({'success': False})


@app.route('/pubkey', methods=['GET', 'POST'])
def publickey():
    username = request.json['username']
    ssh_key = request.json['publicKey']
    remote_address = request.json['remoteAddress']
    connection_id = request.json['connectionId']

    valid = is_valid_key(username, ssh_key)

    app.logger.info(
        '%s connection %s, user %s from %s using ssh key %s',
        'Accepted' if valid else 'Rejected',
        connection_id,
        username,
        remote_address,
        ssh_key,
    )

    return jsonify(success=valid), 200 if valid else 403
