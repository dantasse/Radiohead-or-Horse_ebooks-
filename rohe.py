import os

# http://code.google.com/appengine/docs/python/tools/libraries.html#Django 
from google.appengine.dist import use_library
use_library('django', '1.2')

import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/python-oauth2"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/python-twitter"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/httplib2"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/simplejson"))

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app
import twitter

class MainPage(webapp.RequestHandler):
    def get(self):
        api = twitter.Api()
        statuses = api.GetUserTimeline('Horse_ebooks')
        template_values = {
            'tweets': [s.text for s in statuses]
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
