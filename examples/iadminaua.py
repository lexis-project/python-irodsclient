#!/bin/env python2
import argparse
import sys
import json
import getpass
#import irods
from irods.session import iRODSSession
from irods.manager.collection_manager import CollectionManager

#Creation of user with an auth-name (see iadmin aua, iadmin lua)
#authname is indicated with parameter auth_str
#session.users.create(username, usertype, rodszone, authname)

def main(argv):
    parser = argparse.ArgumentParser(description='pyils: Connect to iRODS with OpenID and Python')
    parser.add_argument('--env-file', required=True, type=str)
    #parser.add_argument('--sess-file', type=argparse.FileType('w'))
    parser.add_argument('newuser', type=str)
    parser.add_argument('usertype', type=str)
    parser.add_argument('userzone', type=str)
    parser.add_argument('userauthname', type=str)

    args = parser.parse_args(argv[1:])
    with open(args.env_file, 'r') as f:
        fc = f.read()
        env = json.loads(fc)

    kwargs = {
        'host': env['irods_host'],
        'port': env['irods_port'],
        'user': env['irods_user_name'],
        'zone': env['irods_zone_name'],
#        'authentication_scheme': 'openid'
    }
    if 'irods_authentication_scheme' in env:
        kwargs['irods_authentication_scheme'] = env['irods_authentication_scheme']
    if 'openid_provider' in env:
        kwargs['openid_provider'] = env['openid_provider']
    if kwargs.get('irods_authentication_scheme', None) in [None, 'native']:
        kwargs['password'] = getpass.getpass('Enter password: ')

    session = iRODSSession(**kwargs)
#create user
    session.users.create(args.newuser, args.usertype, args.userzone, args.authname)

if __name__ == '__main__':
    main(sys.argv)
