#!/bin/env python2
import argparse
import sys
import json
import getpass
#import irods
from irods.session import iRODSSession
from irods.manager.collection_manager import CollectionManager

def main(argv):
    parser = argparse.ArgumentParser(description='pyils: Connect to iRODS with OpenID and Python')
    parser.add_argument('--env-file', required=True, type=str)
    #parser.add_argument('--sess-file', type=argparse.FileType('w'))
    parser.add_argument('path', type=str)
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
    if 'authentication_scheme' in env:
        kwargs['authentication_scheme'] = env['authentication_scheme']
    if 'openid_provider' in env:
        kwargs['openid_provider'] = env['openid_provider']
    if kwargs.get('authentication_scheme', None) in [None, 'native']:
        kwargs['password'] = getpass.getpass('Enter password: ')

    session = iRODSSession(**kwargs)
    coll_manager = CollectionManager(session)
    def ls_coll(coll):
        for data_obj in coll.data_objects:
            print('   ' + data_obj.name)
        for coll_obj in coll.subcollections:
            print('C- ' + coll_obj.name)
    #home_coll = coll_manager.get('/commonssharetestZone/home/' + env['irods_user_name'])
    coll = coll_manager.get(args.path)
    ls_coll(coll)

if __name__ == '__main__':
    main(sys.argv)
