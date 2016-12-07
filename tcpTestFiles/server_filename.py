#Written by Vlatko Klabucar
#Simple HTTP Server. Posts a single image or provides GET information

from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor

import cgi

class UploadImage(Resource):
    def render_GET(self, request):
    	print "getting"
        return '<html><body><p>To upload an image just send me a POST request.</p><p> P.S. don\'t forget the image :)</p></body></html>'

    def render_POST(self, request):
    	print "posting"
    	name = request.getHeader('filename')
    	print name
        file = open("{0}".format(name),"wb")
        file.write(request.content.read())
        return '<html><body>Image uploaded :) </body></html>'

root = Resource()
root.putChild("upload-image", UploadImage())
factory = Site(root)
reactor.listenTCP(8888, factory)
reactor.run()