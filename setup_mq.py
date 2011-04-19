from couchdbkit import Server
from couchdbkit.designer import push


COUCHDB = "http://nettok:2600@ernesto-m.iriscouch.com/"
DB = "mq0"


if __name__ == "__main__":
    server = Server(COUCHDB, use_proxy=True, follow_redirect=True)
    
    db = server.get_or_create_db(DB)
    
    push("./mqdb/_design/message", db)