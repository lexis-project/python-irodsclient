#!/bin/env python2
import argparse
import sys
import time
import json
import os
import getpass
import humanize
from irods.session import iRODSSession
#from irods.manager.collection_manager import CollectionManager

def line_out(s):
    # http://www.termsys.demon.co.uk/vtansi.htm
    sys.stdout.write('\x1b[2K\r')
    sys.stdout.write(str(s))
    sys.stdout.flush()

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
        'zone': env['irods_zone_name']
    }
    if 'irods_authentication_scheme' in env:
        kwargs['irods_authentication_scheme'] = env['irods_authentication_scheme']
    if 'openid_provider' in env:
        kwargs['openid_provider'] = env['openid_provider']
    if kwargs.get('authentication_scheme', None) in [None, 'native']:
        kwargs['password'] = getpass.getpass('Enter password: ')

    session = iRODSSession(**kwargs)
    
    # These checks are sufficient because this code only works if src is a
    # single object, not a collection
    dstpath = args.dstpath
    if dstpath is None:
        # destination was not specified
        dstpath = os.getcwd()
    srcpath = args.srcpath
    src_basename = os.path.basename(srcpath)
    if not dstpath.endswith(src_basename):
        dstpath = os.path.join(dstpath, src_basename)

    remote_obj = session.data_objects.get(srcpath)
    print('reading {} into {}'.format(srcpath, dstpath))
    window_start = 0.0
    window_bytes = 0.0
    total_bytes = 0
    average_rate = 0.0
    check_interval = 1.0 # seconds
    with remote_obj.open('r') as f_in:
        # 2MiB chunks. Somewhat arbitrary, but pretty good in manual tests
        chunk_size = 2 * 1024 * 1024 
        with open(dstpath, 'wb') as f_out:
            window_start = time.time()
            while True:
                chunk = f_in.read(chunk_size)
                if len(chunk) <= 0:
                    break
                total_bytes += len(chunk)
                window_bytes += len(chunk)
                f_out.write(chunk)
                curr_time = time.time()
                if curr_time >= window_start + check_interval:
                    average_rate = 0.6 * average_rate + 0.4 * (window_bytes / (curr_time - window_start))
                    line_out('Total transferred: {} B ({}), Approximate Current Rate: {} B/s ({}/s)'.format(
                            total_bytes, humanize.naturalsize(total_bytes, binary=True),
                            int(average_rate), humanize.naturalsize(average_rate, binary=True)))
                    # reset window stats
                    window_start = time.time()
                    window_bytes = 0.0

    print('\nFinished read')

if __name__ == '__main__':
    exit(main(sys.argv))
