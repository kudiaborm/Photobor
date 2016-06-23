import os
import cgi
import urllib
import webapp2

from google.appengine.ext.webapp import template
from google.appengine.api import images
from google.appengine.ext import ndb
from google.appengine.ext import blobstore


class Photo(ndb.Model):
    title = ndb.StringProperty()
    caption = ndb.TextProperty()
    full_size_image = ndb.BlobProperty()

def guestbook_key(guestbook_name=None):
    """Constructs a Datastore key for a Guestbook entity with guestbook_name."""
    return ndb.Key('Thumbnail', guestbook_name or 'default_thumbnail')


class Thumbnail(webapp2.RequestHandler):
    def get(self):
        if self.request.get("id"):
            #photo = Photo.get_by_id(int(self.request.get("id")))
            key = blobstore.create_gs_key(self.request.get("id"))
            blobstore
            if key:
                img = images.get_serving_url(key, size=600)

                self.response.headers['Content-Type'] = 'image/jpeg'
                self.response.out.write(img)
                return

        # Either "id" wasn't provided, or there was no image with that ID
        # in the datastore.
        self.error(404)
        
class MainPage(webapp2.RequestHandler):
    def get(self):
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))        

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/pho', Thumbnail)])
#spp.append(('/image', GetImage))
