from google.appengine.ext import db

class Quote(db.Model):
    text = db.StringProperty()
    is_radiohead = db.BooleanProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)

class Guess(db.Model):
    quote = db.ReferenceProperty(reference_class=Quote)
    guessed_radiohead = db.BooleanProperty()
    date_added = db.DateTimeProperty(auto_now_add=True)
