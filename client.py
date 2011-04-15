from couchdbkit import Server, Consumer


COUCHDB = "http://nettok:2600@ernesto-m.iriscouch.com/"
DB = "mq0"


def consume_msg(msg):
    print msg


if __name__ == "__main__":
    server = Server(COUCHDB)
    
    ## TODO: use config file to get these
    server.res.client.use_proxy = True
    server.res.client.follow_redirect = True
    #####
    
    db = server.get_or_create_db(DB)
    
    ## TODO: again for db!?
    db.res.client.use_proxy = True
    db.res.client.follow_redirect = True
    #####
    
    consumer = Consumer(db)
    consumer.wait(consume_msg)#, filter_name="designname/filtername")
