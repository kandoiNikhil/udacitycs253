import webapp2
import jinja2
import os
###########################################################
################ Global Variables ########################
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
loader = jinja2.FileSystemLoader(template_dir)
autoescape = True
jinja_env = jinja2.Environment(loader, autoescape)
###########################################################


class Handler(webapp2.RequestHandler):

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.response.out.write(self.render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)


class MainPage(Handler):

    def get(self):
        self.render('index.html')


class Login(Handler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        result = db.GqlQuery("Select * from User where username = '%s'" %username)
