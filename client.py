from couchdbkit import Server, Consumer
from restkit.errors import NoMoreData

import config as cfg


class ReconnectingChangesWaiter(object):
    def __init__(self, db, since=0, filter_name=None):
        self.db = db
        self.since = since
        self.filter_name = filter_name

    def wait(self, callback):
        consumer = Consumer(db)

        def process(change):
            seq = change.get('seq')
            last_seq = change.get('last_seq')

            if seq is not None:
                if seq > self.since:
                    self.since = seq
                    
                callback(change)
            elif last_seq is not None:
                self.since = last_seq
        
        while True:
            try:
                consumer.wait(process, since = self.since, filter_name = self.filter_name)
            except NoMoreData:
                pass


if __name__ == "__main__":
    import sys
    
    server = Server(cfg.server)
    
    db = server.get_or_create_db(cfg.db)

    rcw = ReconnectingChangesWaiter(db)
    rcw.wait(lambda change: sys.stdout.write(str(change) + '\n'))
