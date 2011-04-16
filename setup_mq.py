from couchdbkit import Server
from couchdbkit.designer import push

from utils import patch_restkit
patch_restkit()


COUCHDB = "http://nettok:2600@ernesto-m.iriscouch.com/"
DB = "mq0"


if __name__ == "__main__":
    server = Server(COUCHDB)
    
    db = server.get_or_create_db(DB)
    
    push("./mqdb/_design/message", db)