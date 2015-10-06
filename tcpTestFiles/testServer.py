from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

import cgi

class FormPage(Resource):
    def render_GET(self, request):
    	print "getting!"
        return '<html><body><p>To upload an image just send me a POST request.</p><p> P.S. don\'t forget the image :)</p></body></html>'

    def render_POST(self, request):
    	print "posting!"
    	file = open("uploaded-image.jpg","wb")
        file.write(request.content.read())
        return '<html><body>Image uploaded :) </body></html>'

root = Resource()
root.putChild("form", FormPage())  #user accesses website through localhost:8880/form
factory = Site(root)
reactor.listenTCP(8880, factory)
reactor.run()

#Original code from Twisted Documentation

# from twisted.web.server import Site
# from twisted.web.resource import Resource
# from twisted.internet import reactor

# import cgi

# class FormPage(Resource):
#     def render_GET(self, request):
#         return '<html><body><form method="POST"><input name="the-field" type="text" /></form></body></html>'

#     def render_POST(self, request):
#         return '<html><body>You submitted: %s</body></html>' % (cgi.escape(request.args["the-field"][0]),)

# root = Resource()
# root.putChild("form", FormPage())
# factory = Site(root)
# reactor.listenTCP(8880, factory)
# reactor.run()