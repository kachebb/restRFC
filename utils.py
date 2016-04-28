def getIP(req):
    """
        Returns the str IP addr from the request.
        NOTE: This is required because when we use nginx servers
        it is used as a proxy, so the REAL IP addr is stored in a HTTP header
        called 'X-Real-IP', so we need to check for this first, otherwise the
        request.getClientIP() is always going to return 'localhost' to us.
    """
    ip = req.received_headers.get('X-Real-IP')
    if(ip is None):
        return req.getClientIP()
    else:
        return ip
