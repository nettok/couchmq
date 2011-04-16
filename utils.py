def patch_restkit():
    from restkit import Client

    Client.use_proxy = True
    Client.follow_redirect = True