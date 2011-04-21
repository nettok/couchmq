from couchdbkit import Server, Consumer
from restkit.errors import NoMoreData

import config as cfg


class ReconnectingChangesWaiter(object):
    def __init__(self, db):
        self.db = db

    def wait(self, callback, **params):
        if 'since' not in params:
            params['since'] = 0
            
        self._params = params
    
        consumer = Consumer(db)

        def process(change):
            seq = change.get('seq')
            last_seq = change.get('last_seq')

            if seq is not None:
                if seq > self._params['since']:
                    self._params['since'] = seq
                    
                callback(change)
            elif last_seq is not None:
                self._params['since'] = last_seq
        
        while True:
            try:
                consumer.wait(process, **self._params)
            except NoMoreData:
                pass


if __name__ == "__main__":
    import sys
    
    server = Server(cfg.server)
    
    db = server.get_or_create_db(cfg.db)

    rcw = ReconnectingChangesWaiter(db)
    rcw.wait(lambda change: sys.stdout.write(str(change) + '\n'),
             filter = 'message/state', state = 'available')
