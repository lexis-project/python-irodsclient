from __future__ import absolute_import
import logging
import threading

from irods import DEFAULT_CONNECTION_TIMEOUT
from irods.connection import Connection

logger = logging.getLogger(__name__)


class Pool(object):
    currentAuth=None
    def __init__(self, account, block_on_authURL=True):
        self.account = account
        self.block_on_authURL=block_on_authURL
        self._lock = threading.RLock()
        self.active = set()
        self.idle = set()
        self.connection_timeout = DEFAULT_CONNECTION_TIMEOUT

    def get_connection(self):
        with self._lock:
            try:
                conn = self.idle.pop()
            except KeyError:
                conn = Connection(self, self.account, block_on_authURL=self.block_on_authURL)
            self.active.add(conn)
        logger.debug('num active: {}'.format(len(self.active)))
        return conn

    def release_connection(self, conn, destroy=False):
        with self._lock:
            if conn in self.active:
                self.active.remove(conn)
                if not destroy:
                    self.idle.add(conn)
            elif conn in self.idle and destroy:
                self.idle.remove(conn)
        logger.debug('num idle: {}'.format(len(self.idle)))
