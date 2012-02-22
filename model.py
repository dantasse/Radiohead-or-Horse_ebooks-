from google.appengine.ext import db

class Quote(db.Model):
    text = db.StringProperty()
    isRadiohead = db.BooleanProperty()
    dateAdded = db.DateTimeProperty(auto_now_add=True)
    # random value to allow picking a random quote from the datastore
    random_number = db.FloatProperty()

class Guess(db.Model):
    quote = db.ReferenceProperty(reference_class=Quote)
    guessedRadiohead = db.BooleanProperty()
    dateAdded = db.DateTimeProperty(auto_now_add=True)
