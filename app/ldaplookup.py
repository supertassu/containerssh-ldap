from flask import current_app
from typing import List
import ldap


def connect(server: str, username: str, password: str, tls: bool):
    conn = ldap.initialize('ldap://%s:389' % server)
    conn.set_option(ldap.OPT_NETWORK_TIMEOUT, 3.0)
    conn.set_option(ldap.OPT_TIMEOUT, 5)
    conn.protocol_version = ldap.VERSION3
    if tls:
        conn.start_tls_s()
    conn.simple_bind_s(username, password)
    return conn


def robust_connect(servers: List[str], user: str, password: str, tls: bool, position=0):
    try:
        return connect(servers[position], user, password, tls)
    except ldap.SERVER_DOWN:
        if position == len(servers) - 1:
            return
        position += 1
        return robust_connect(servers, user, password, tls, position)


def get_connection():
    config = current_app.config['LDAP']
    return robust_connect(
        config['SERVERS'], config['BIND_USERNAME'], config['BIND_PASSWORD'], config['USE_STARTTLS']
    )


def get_user_keys(conn, user):
    try:
        response = conn.search_s(
            user,
            ldap.SCOPE_BASE,
            filterstr=current_app.config['LDAP']['FILTER'],
            attrlist=['sshPublicKey'],
        )
    except ldap.NO_SUCH_OBJECT:
        response = None
    if response:
        return response[0][1].get(current_app.config['LDAP']['ATTRIBUTE'], [])
    return []


def is_valid_key(username: str, key_to_check: str) -> bool:
    connection = get_connection()
    username_to_search = current_app.config['LDAP']['USERNAME_DN'] % username

    given_key_type, given_key_data, *_ = key_to_check.split(' ')

    for key in get_user_keys(connection, username_to_search):
        this_key_type, this_key_data, *_ = key.decode('utf8').strip().split(' ')
        if given_key_type == this_key_type and given_key_data == this_key_data:
            return True
    return False
