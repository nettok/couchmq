from couchdbkit import Server
from couchdbkit.designer import push


COUCHDB = "http://nettok:2600@ernesto-m.iriscouch.com/"
DB = "mq0"


if __name__ == "__main__":
    server = Server(COUCHDB)
    
    ## TODO: use config file to get these
    server.res.client.use_proxy = True
    server.res.client.follow_redirect = True
    #####
    
    db = server.get_or_create_db(DB)
    
    ## TODO: Otra vez, ahora para la db!?
    db.res.client.use_proxy = True
    db.res.client.follow_redirect = True
    #####
    
    push("./mqdb/_design/message", db)