from couchdbkit import Server, Consumer

from restkit.errors import NoMoreData


COUCHDB = "http://nettok:2600@ernesto-m.iriscouch.com/"
DB = "mq0"


class ReconnectingChangesWaiter(object):
    def __init__(self, db, since=0, filter_name=None):
        self.db = db
        self.since = since
        self.filter_name = filter_name

    def wait(self, callback):
        consumer = Consumer(db)

        def process(change):
            if change['seq'] > self.since:
                self.since = change['seq']

            callback(change)
        
        while True:
            try:
                consumer.wait(process, since = self.since, filter_name = self.filter_name)
            except NoMoreData:
                pass


if __name__ == "__main__":
    import sys
    
    server = Server(COUCHDB, use_proxy=True, follow_redirect=True)
    
    db = server.get_or_create_db(DB)

    rcw = ReconnectingChangesWaiter(db)
    rcw.wait(lambda change: sys.stdout.write(str(change) + '\n'))