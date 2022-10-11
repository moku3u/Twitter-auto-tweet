class TwitterAccessDenied(Exception):
    #Returned when the status code is 403
    pass

class TwitterRateLimit(Exception):
    #Returned when the status code is 429
    pass

class TwitterInternalServerError(Exception):
    #Returned when the status code is 500 or more
    pass

class TwitterBadRequest(Exception):
    #Returned when the status code is 400
    pass

class TwitterBadRequest(Exception):
    #Returned when the status code is 400
    pass

class TwitterJavascriptNotFound(Exception):
    #Returned when there is no main.js in html
    pass