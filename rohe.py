
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/python-oauth2"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/python-twitter"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/httplib2"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/httplib2/python2/"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/httplib2/python2/httplib2"))
sys.path.append(os.path.join(os.path.dirname(__file__), "lib/httplib2/build/lib.linux-i686-2.7/httplib2"))

import twitter
from model import Quote
from model import Guess
import random
import logging
import re
import webapp2
import jinja2

class MainPage(webapp2.RequestHandler):
    def get(self, correct=None):
        message = ''
        if correct == False:
            message = 'No I am afraid that is not correct'
        elif correct == True:
            message = 'Yes indeed that is correct'
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
        template = jinja_environment.get_template('index.html')
        self.response.out.write(template.render(template_values))

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

class GetMoreQuotes(webapp2.RequestHandler):
    def get(self):
        # cache: http://code.google.com/p/python-twitter/issues/detail?id=59
        api = twitter.Api(cache=None)
        countstr = self.request.get('num_quotes')
        count = int(countstr) if countstr else 5
 
        statuses = api.GetUserTimeline('Horse_ebooks', count=count)

        num_successful_quotes = 0
        lyrics_string = open('scrape_radiohead/all_lyrics.txt').read()
        all_radiohead_lyrics = re.split('\s+', lyrics_string)
        for status in statuses:
            # clean up each Horse_ebooks tweet
            horse_text = status.text
            # strip out URLs
            horse_text = re.sub('http://\S*', '', horse_text)
            horse_text = re.sub('\n', '', horse_text)
            horse_words = re.split('\s+', horse_text)
            if len(horse_words) < 3:
                continue

            # add it to the datastore 
            horse_quote = Quote()
            horse_quote.text = horse_text
            horse_quote.is_radiohead = False
            horse_quote.put()

            # also add a snippet of Radiohead lyrics of the same size
            # sometimes adds an extra one if the text ends in whitespace
            # don't really care to figure out why
            num_words = len(horse_words)
            start_index = random.randrange(len(all_radiohead_lyrics) - num_words)
            radiohead_words = all_radiohead_lyrics[start_index:start_index + num_words]
            # make capitalization same as the Horse_ebooks tweet
            for i in range(len(horse_words)):
                if horse_words[i].isupper():
                    radiohead_words[i] = radiohead_words[i].upper()
                elif horse_words[i].istitle():
                    radiohead_words[i] = radiohead_words[i].title()
 
            radiohead_text = ' '.join(radiohead_words)

            # save the radiohead quote to the datastore
            radiohead_quote = Quote()
            radiohead_quote.text = radiohead_text
            radiohead_quote.is_radiohead = True
            radiohead_quote.put()

            logging.info('adding this horse_ebooks tweet: ' + horse_text)
            logging.info('adding this corresponding radiohead: ' + radiohead_text)
            num_successful_quotes += 1
 
        self.response.out.write(\
            'Got more quotes. This many: ' + str(num_successful_quotes))
        logging.info('Added this many quotes each: ' + str(num_successful_quotes))


jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

app = webapp2.WSGIApplication([('/', MainPage),
                                      ('/get_more_quotes', GetMoreQuotes)])

