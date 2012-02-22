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
from model import Quote
import random
import logging

class MainPage(webapp.RequestHandler):
    def get(self):
        # http://code.google.com/p/python-twitter/issues/detail?id=59
#        api = twitter.Api(cache=None)
#        statuses = api.GetUserTimeline('Horse_ebooks')

        # Get a random quote. If the number of quotes gets large, this
        # might get slow.
        num_quotes = Quote.all(keys_only=True).count()
        offset = random.randrange(num_quotes)
        quote = Quote.all().fetch(1, offset)[0]
        template_values = {
            'quote' : quote.text
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
 
        # q1 = model.Quote()
        # q1.text = "Radiohead Quote 1"
        # q1.isRadiohead = True
        # q1.put() 
        # g1 = model.Guess()
        # g1.quoteId = q1
        # g1.guessedRadiohead = False
        # g1.put()

application = webapp.WSGIApplication(
                                     [('/', MainPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
