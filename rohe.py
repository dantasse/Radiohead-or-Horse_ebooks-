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
from model import Guess
import random
import logging

class MainPage(webapp.RequestHandler):
    def get(self, correct=None):
        # http://code.google.com/p/python-twitter/issues/detail?id=59
#        api = twitter.Api(cache=None)
#        statuses = api.GetUserTimeline('Horse_ebooks')

        message = ''
        if correct == False:
            message = 'Not correct'
        elif correct == True:
            message = 'Correct' 
        # Get a random quote. If the number of quotes gets large, this
        # might get slow.
        num_quotes = Quote.all(keys_only=True).count()
        offset = random.randrange(num_quotes)
        quote = Quote.all().fetch(1, offset)[0]
        template_values = {
            'message': message,
            'quote': quote.text,
            'quote_id': quote.key().id()
        }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
 
    def post(self):
        quote_id = self.request.get('quote_id')
        quote = Quote.get_by_id(int(quote_id))
        guessed_radiohead = bool(self.request.get('radiohead'))

        guess = Guess()
        guess.quote = quote
        guess.guessed_radiohead = guessed_radiohead
        guess.put()

        if (quote.is_radiohead == guessed_radiohead):
            self.get(correct=True)
        else:
            self.get(correct=False)

class GetMoreQuotes(webapp.RequestHandler):
    def get(self):
        logging.info('Getting more quotes now')
        self.response.out.write('Got more quotes.')

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/get_more_quotes', GetMoreQuotes)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
