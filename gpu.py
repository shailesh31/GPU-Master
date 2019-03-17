from google.appengine.ext import ndb

class GPU(ndb.Model):
    name = ndb.StringProperty()
    manufacturer= ndb.StringProperty()
    dateissued= ndb.DateProperty()
    geometryShader = ndb.BooleanProperty()
    tesselationShader = ndb.BooleanProperty()
    shaderInt16 = ndb.BooleanProperty()
    sparseBinding = ndb.BooleanProperty()
    textureCompressionETCS = ndb.BooleanProperty()
    vertexPipelineStoresAndAtomics = ndb.BooleanProperty()
