import os
import webapp2
import jinja2

from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
from myuser import MyUser
from gpu import GPU


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class update(webapp2.RequestHandler):
    def get(self):

        welcome= 'welcome back'

        user=users.get_current_user()

        if users:
            url = users.create_logout_url('/')
            url_string='logout'

        else:
            url=''
            users.create_logout_url(self.request.uri)

        url_string='login'

        name = self.request.get('name')
        gpu_key = ndb.Key('GPU', name)
        gpu_query = gpu_key.get()

        if gpu_query is None:
            self.redirect('/')
            return



        if (gpu_query.geometryShader):
            geometryShader = 'checked'
        else:
            geometryShader =''
        if (gpu_query.tesselationShader):
            tesselationShader= 'checked'
        else:
            tesselationShader =''
        if (gpu_query.shaderInt16):
            shaderInt16 = 'checked'
        else:
            shaderInt16 =''
        if (gpu_query.sparseBinding):
            sparseBinding = 'checked'
        else:
            sparseBinding =''
        if (gpu_query.textureCompressionETCS):
            textureCompressionETCS = 'checked'
        else:
            textureCompressionETCS =''
        if (gpu_query.vertexPipelineStoresAndAtomics):
            vertexPipelineStoresAndAtomics = 'checked'
        else:
            vertexPipelineStoresAndAtomics =''

        template_values = {
            'url': url,
            'url_string': url_string,
            'user': user,
            'welcome': welcome,
            'logout_url': users.create_login_url(self.request.uri),
            'my_gpu': gpu_query,
            'geometryShader': geometryShader,
            'tesselationShader': tesselationShader,
            'shaderInt16': shaderInt16,
            'sparseBinding': sparseBinding,
            'textureCompressionETCS': textureCompressionETCS,
            'vertexPipelineStoresAndAtomics': vertexPipelineStoresAndAtomics
        }
        template = JINJA_ENVIRONMENT.get_template('update.html')
        self.response.write(template.render(template_values))

    def post(self):
        action = self.request.get('button')
        if action == 'UPDATE DATASTORE':
            name = self.request.get('name')
            gpu_key = ndb.Key('GPU', name)
            my_gpu = gpu_key.get()

            my_gpu.manufacturer = self.request.get('manufacturer')
            my_gpu.dateissued = datetime.strptime(self.request.get('dateissued'), '%Y-%m-%d' )
            #logger.info(dateissued)
            my_gpu.geometryShader = self.request.POST.get('geometryShader') == 'on'
            my_gpu.tesselationShader = self.request.POST.get('tesselationShader') == 'on'
            my_gpu.shaderInt16 = self.request.POST.get('shaderInt16') == 'on'
            my_gpu.sparseBinding = self.request.POST.get('sparseBinding') == 'on'
            my_gpu.textureCompressionETCS = self.request.POST.get('textureCompressionETCS') == 'on'
            my_gpu.vertexPipelineStoresAndAtomics = self.request.POST.get('vertexPipelineStoresAndAtomics') == 'on'
            my_gpu.put()
            self.redirect('/')

        elif self.request.get('button') == 'CANCEL':
            self.redirect('/')




