from pyramid.events import NewResponse, subscriber

@subscriber(NewResponse)
def handleCORS(event):
    event.response.headerlist.append(("Access-Control-Allow-Origin", "http://www.lukchic.com")) #http://localhost:8000
    event.response.headerlist.append(("Access-Control-Allow-Methods", "GET, PUT, POST, DELETE"))
    event.response.headerlist.append(("Access-Control-Expose-Headers", "X-CSRF-token"))
    event.response.headerlist.append(("Access-Control-Allow-Credentials", 'true'))
    event.response.headerlist.append(("Access-Control-Allow-Headers", 'X-CSRF-token'))
