"""
Implementing the general bottle setup with the additional feature to support
a threaded (non blocking) execution
"""

from gevent import monkey
from database import _ParseConfig
import logging
import threading
import bottle
import website

# Apply GEVENT patches to bottle server to enable asynchronous functionality
monkey.patch_all()


log = logging.getLogger(__name__)


class ServerThread(threading.Thread):
    def __init__(self, server, **kwargs):
        log.info("initalizing threaded server")
        self.server = server
        threading.Thread.__init__(self, **kwargs)

    def stop(self, wait=True, timeout=None):
        log.info("shutdown threaded server")
        self.server.srv.close()
        if wait:
            self.join(timeout=timeout)


# @bottle.error(500)
def _error_handler_500(error):
    """ Log internal errors and call the default handler. """
    log.error("http error 500:\n%s\n%s", error.exception, error.traceback)
    return bottle.app.default.default_error_handler(error)


def _run(**kwargs):
    bottle.run(**kwargs)


def run(blocking=True):
    cfg = _ParseConfig()
    cfg_webserver = cfg['webserver']
    port = cfg_webserver.get('port')
    server = bottle.GeventServer(host=cfg_webserver.get('host'), port=cfg_webserver.get('port'))
    kwargs = {
        "server": server,
        "quiet": not cfg.get('debug'),
        "debug": cfg.get('debug'),
    }
    if blocking:
        log.info("start blocking http server")
        _run(**kwargs)
    else:
        log.info("start non-blocking http server")
        thread = ServerThread(server, target=_run, kwargs=kwargs)
        thread.start()
        return thread
