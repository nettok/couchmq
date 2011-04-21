from functools import partial

from couchdbkit import Server, Consumer
from couchdbkit.exceptions import ResourceConflict
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
                
                
def reserve(db, change):
    try:
        body = db.res.put('_design/message/_update/reserve/%s' % change['id']).json_body
    except ResourceConflict:
        body = 'conflict while updating'

    if body == 'ok':
        print 'reserved:', change['id']
    else:
        print 'error:', body, change['id']

if __name__ == "__main__":
    import sys
    
    server = Server(cfg.server)
    
    db = server.get_or_create_db(cfg.db)

    rcw = ReconnectingChangesWaiter(db)
    rcw.wait(partial(reserve, db), filter = 'message/state', state = 'available')
