import os
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from gpu import GPU
from datetime import datetime
from Editpage import Editpage
from update import update


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user == None:
            template_values = {
                'login_url' : users.create_login_url(self.request.uri)
            }

            template = JINJA_ENVIRONMENT.get_template('mainpage_guest.html')
            self.response.write(template.render(template_values))
            return

        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if myuser == None:
            myuser = MyUser(id=user.user_id())
            myuser.put()
        gpu_query = GPU().query().fetch()

        template_values = {
    'logout_url' : users.create_logout_url(self.request.uri),
    'gpu' : gpu_query
}

        template = JINJA_ENVIRONMENT.get_template('mainpage.html')
        self.response.write(template.render(template_values))
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        action = self.request.get('button')
        if action == 'Add Information':
            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            #date_gpu = datetime.strptime(self.request.get('dateissued'), '%Y-%m-%d').date()
            #date_gpu_calender = calendar.timegm(date_gpu.timetuple())
            #dateissued = datetime.utcfromtimestamp(date_gpu_calender)
            dateissued = self.request.get('dateissued')
            #logger.info(dateissued)
            geometryShader = self.request.POST.get('geometryShader') == 'on'
            tesselationShader = self.request.POST.get('tesselationShader') == 'on'
            shaderInt16 = self.request.POST.get('shaderInt16') == 'on'
            sparseBinding =  self.request.POST.get('sparseBinding') == 'on'
            textureCompressionETCS = self.request.POST.get('textureCompressionETCS') == 'on'
            vertexPipelineStoresAndAtomics = self.request.POST.get('vertexPipelineStoresAndAtomics') == 'on'
            if name == '':
                self.redirect('/')
            elif manufacturer == '':
                self.redirect('/')
            elif dateissued == '':
                self.redirect('/')
            else:

                gpu_list = GPU.query()
                if geometryShader:
                    gpu_list.filter(GPU.geometryShader == True)

                if tesselationShader:
                    gpu_list.filter(GPU.tesselationShader==True)

                if shaderInt16:
                    gpu_list.filter(GPU.shaderInt16==True)

                if sparseBinding:
                    gpu_list.filter(GPU.sparseBinding==True)

                if textureCompressionETCS:
                    gpu_list.filter(GPU.textureCompressionETCS==True)

                if vertexPipelineStoresAndAtomics:
                    gpu_list.filter(GPU.vertextPipelineStoresandAtomics==True)
                gpu_list = gpu_list.fetch()

                user = users.get_current_user()

                mygpu_key = ndb.Key('GPU', name)
                mygpu = mygpu_key.get()

                mygpu.gpu.append(gpu_list)
                mygpu.put()
                template_values = {

                    'gpu_list': gpu_list,
                    'geometryShader': geometryShader,
                    'tesselationShader': tesselationShader,
                    'shaderInt16': shaderInt16,
                    'sparseBinding': sparseBinding,
                    'textureCompressionETCS': textureCompressionETCS,
                    'vertextPipelineStoresandAtomics': vertexPipelineStoresAndAtomics
                    }

                template = JINJA_ENVIRONMENT.get_template('mainpage.html')
                self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content - Type'] = 'text / html'
        action = self.request.get('button')
        if action == 'Add Information':


            name = self.request.get('name')
            manufacturer = self.request.get('manufacturer')
            dateissued = self.request.get('dateissued')
            geometryShader = self.request.POST.get('geometryShader') == 'on'
            tesselationShader = self.request.POST.get('tesselationShader') == 'on'
            shaderInt16 = self.request.POST.get('shaderInt16') == 'on'
            sparseBinding = self.request.POST.get('sparseBinding')  == 'on'
            textureCompressionETCS = self.request.POST.get('textureCompressionETCS') == 'on'
            vertexPipelineStoresAndAtomics = self.request.POST.get('vertexPipelineStoresAndAtomics') == 'on'
            if name == '':
                self.redirect('/')
            elif manufacturer == '':
                self.redirect('/')
            elif dateissued =='':
                self.redirect('/')
            else:
                user = users.get_current_user()

                myuser_key = ndb.Key('MyUser', user.user_id())
                myuser = myuser_key.get()
                gpu_key = ndb.Key('GPU',name)
                my_gpu = gpu_key.get()
                if my_gpu == None:
                    new_gpu = GPU(id=name,name=name, manufacturer=manufacturer,dateissued=datetime.strptime(dateissued,'%Y-%m-%d').date(),geometryShader=geometryShader, tesselationShader=tesselationShader, shaderInt16=shaderInt16, sparseBinding=sparseBinding, textureCompressionETCS=textureCompressionETCS, vertexPipelineStoresAndAtomics=vertexPipelineStoresAndAtomics)
                    myuser.gpu.append(new_gpu)
                    new_gpu.put()

                    self.redirect('/')
                else:
                    template_values = {
                        'msg' :  'Sorry !! You cannot create GPU with already existing name. '
                    }
                    template= JINJA_ENVIRONMENT.get_template('mainpage.html')
                    self.response.write(template.render(template_values))

        elif action == 'Gpu Feature Index':
            geometryShader = bool(self.request.get('geometryShader'))
            tesselationShader = bool(self.request.get('tesselationShader'))
            shaderInt16 = bool(self.request.get('shaderInt16'))
            sparseBinding = bool(self.request.get('sparseBinding'))
            textureCompressionETCS = bool(self.request.get('textureCompressionETCS'))
            vertexPipelineStoresAndAtomics = bool(self.request.get('vertexPipelineStoresAndAtomics'))

            my_gpu = GPU.query()

            if geometryShader:
                my_gpu = my_gpu.filter(GPU.geometryShader == True)
            if tesselationShader:
                my_gpu = my_gpu.filter(GPU.tesselationShader == True)
            if shaderInt16:
                my_gpu = my_gpu.filter(GPU.shaderInt16 == True)
            if sparseBinding:
                my_gpu = my_gpu.filter(GPU.sparseBinding == True)
            if textureCompressionETCS:
                my_gpu = my_gpu.filter(GPU.textureCompressionETCS == True)
            if vertexPipelineStoresAndAtomics:
                my_gpu = my_gpu.filter(GPU.vertexPipelineStoresAndAtomics == True)

            template_values = {
                'gpu': my_gpu
            }
            template = JINJA_ENVIRONMENT.get_template('mainpage.html')
            self.response.write(template.render(template_values))

        elif action == 'Compare':

            my_gpu = {}


            gpu_id = self.request.get('gpuID', allow_multiple=True)

            for i in range(len(gpu_id)):
               my_gpu[i] = GPU.query()

               my_gpu[i] = my_gpu[i].filter(GPU.name == gpu_id[i])

            template_values = {
                'gpu' : my_gpu,
                'val' : len(gpu_id)
            }

            template = JINJA_ENVIRONMENT.get_template('Compare.html')
            self.response.write(template.render(template_values))




app = webapp2.WSGIApplication([
        ('/', MainPage), ('/Editpage', Editpage),
        ('/update', update)
    ], debug=True)
