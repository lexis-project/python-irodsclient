#!/bin/env python2
import argparse
import sys
import json
import os
import getpass
#import irods
from irods.session import iRODSSession
from irods.manager.collection_manager import CollectionManager

def main(argv):
    parser = argparse.ArgumentParser(description='pyiget: Get an iRODS file with Python')
    parser.add_argument('--env-file', required=True, type=str)
    #parser.add_argument('--sess-file', type=argparse.FileType('w'))
    parser.add_argument('srcpath', type=str,
            help='iRODS path to get')
    parser.add_argument('dstpath', type=str, nargs='?',
            help='Local path to write to. Defaults to cwd.')
    args = parser.parse_args(argv[1:])
    with open(args.env_file, 'r') as f:
        fc = f.read()
        env = json.loads(fc)

    kwargs = {
        'host': env['irods_host'],
        'port': env['irods_port'],
        'user': env['irods_user_name'],
        'zone': env['irods_zone_name'],
    #    'authentication_scheme': 'openid'
    }
    #if 'openid_provider' in env:
    #    kwargs['openid_provider'] = env['openid_provider']
    if kwargs.get('authentication_scheme', None) in [None, 'native']:
        kwargs['password'] = getpass.getpass('Enter password: ')

    session = iRODSSession(**kwargs)
    
    # These checks are sufficient because this code only works if src is a
    # single object, not a collection
    dstpath = args.dstpath
    if dstpath is None:
        # destination was specified
        dstpath = os.getcwd()
    srcpath = args.srcpath
    src_basename = os.path.basename(srcpath)
    if not dstpath.endswith(src_basename):
        dstpath = os.path.join(dstpath, src_basename)
    print('reading {} into {}'.format(srcpath, dstpath))

    remote_obj = session.data_objects.get(args.srcpath)
    with remote_obj.open('r') as f_in:
        chunk_size = 1024 * 64
        with open(dstpath, 'wb') as f_out:
            while True:
                chunk = f_in.read(chunk_size)
                if len(chunk) <= 0:
                    break
                f_out.write(chunk)

    #home_coll = coll_manager.get('/commonssharetestZone/home/' + env['irods_user_name'])
    #coll = coll_manager.get(args.path)
    #ls_coll(coll)

if __name__ == '__main__':
    main(sys.argv)
