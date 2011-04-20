from couchdbkit import Server
from couchdbkit.designer import push


COUCHDB = "http://localhost:5984"
DB = "mq0"


if __name__ == "__main__":
    server = Server(COUCHDB)
    
    db = server.get_or_create_db(DB)
    
    push("./mqdb/_design/message", db)
