from couchdbkit import Server
from couchdbkit.designer import push

import config as cfg


if __name__ == "__main__":
    server = Server(cfg.server)
    
    db = server.get_or_create_db(cfg.db)
    
    push("./mqdb/_design/message", db)
