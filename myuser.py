from google.appengine.ext import ndb
from gpu import GPU

class MyUser(ndb.Model):
    username = ndb.StringProperty()
    gpu = ndb.StructuredProperty(GPU, repeated=True)


