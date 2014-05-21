import os
import re
import webapp2
import jinja2
from google.appengine.ext import db
import hmac
import random
import string
import hashlib
def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(10))
def make_pw_hash(name,pw,salt=None):
	if not salt:
		salt=make_salt()
	h = hashlib.sha256(name+pw+salt).hexdigest()
	return '%s,%s'%(h,salt)
def valid_pw(name,pw,h):
	salt = h.split(',')[1]
	return h == make_pw_hash(name,pw,salt)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape= True)

secret ="kjasbdf3098r2yiwbfsaboibdsaf3298"
def create_hash(value):
	hash_value = hmac.new(secret,value).hexdigest()
	return '%s|%s'%(value,hash_value)
def check_hash(value):
	val=value.split('|')[0]
	if value == create_hash(val):
		return True
	else:
		return False
class Handler(webapp2.RequestHandler):
	def render_str(self,template,**params):
		t = jinja_env.get_template(template)
		return t.render(params)
	def render(self,template,**kw):
		self.response.out.write(self.render_str(template, **kw))
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)



class User(db.Model):
	username=db.StringProperty(required=True)
	password=db.StringProperty(required=True)
	email=db.StringProperty()

class Signup(Handler):
	def get(self):
		self.render('register.html')

	def post(self):
		username = self.request.get('username')
		password = self.request.get('password')
		verify = self.request.get('verify')
		email = self.request.get('email')
		error_username=""
		error_password=""
		error_verify=""
		error_email=""
		correct=True
		if not valid_username(username):
			error_username="This is not a valid username"
			correct=False
		if not valid_password(password):
			error_password="This is not a valid password"
			correct=False
		if not valid_email(email):
			correct=False
			error_email="This is not a valid email id"
		if verify!=password:
			error_verify="The Passwords do not match"
			correct=False
		if correct:
			query="select * from User where username = '%s'"%username
			present = db.GqlQuery(query)
			if present.count()>=1:
				error_username = "This username already exists"
				self.render('register.html',username=username,password="",verify="",email=email,error_username=error_username,error_password=error_password,error_email=error_email,error_verify=error_verify)

			else:
				password = make_pw_hash(username,password)
				user=User(username=username,password=password,email=email)
				user.put()
				self.response.headers.add_header('Set-Cookie','user-id=%s;Path=/'%create_hash(str(user.key().id())))
				self.redirect('/unit4/welcome')


		else:
			self.render('register.html',username=username,password="",verify="",email=email,error_username=error_username,error_password=error_password,error_email=error_email,error_verify=error_verify)

class Welcome(Handler):
	def get(self):
		user_id = self.request.cookies.get('user-id')
		if user_id is None:
				self.redirect('/unit4/signup')
		elif not check_hash(user_id):
				self.redirect('/unit4/signup')
		else:	
			user = User.get_by_id(int(user_id.split('|')[0]))
			if user is None:
				self.redirect('/unit4/signup')
			else:
				self.response.out.write('Welcome %s'%user.username)
	

class Login(Handler):
	def get(self):
		self.render('login.html')
	def post(self):
		username  = self.request.get('username')
		password = self.request.get('password')
		query  = "select * from User where username='%s'"%username
		results = db.GqlQuery(query)
		error_username=""
		error_password=""
		if results.count() == 0:
			error_username = "No such username exists"
			self.render('login.html',username=username,password="",error_username=error_username,error_password=error_password)
		elif results.count() ==1:
			for user in results:		
				if valid_pw(username,password,user.password):
					self.response.headers.add_header('Set-Cookie','user-id=%s;Path=/'%create_hash(str(user.key().id())))
					self.redirect('/unit4/welcome')
				else:
					error_password = "The Password does not match"
					self.render('login.html',username=username,password="",error_username=error_username,error_password=error_password)
		else:
			self.rediect('/unit4/error')

class Logout(Handler):
	def get(self):
		self.response.headers["Set-Cookie"]="user-id=;path=/"
		self.redirect('/unit4/signup')
class Error(Handler):
	def get(self):
		self.render('error.html')
class DeleteStuff(Handler):
	def get(self):
		q=db.GqlQuery("Select * from User")
		results=q.fetch(100)
		db.delete(results)
		self.response.out.write('ALL USers Deleted')
app = webapp2.WSGIApplication([('/unit4/signup', Signup),                           
 ('/unit4/welcome', Welcome),('/unit4/delete',DeleteStuff),('/unit4/login',Login),('/unit4/logout',Logout)],debug=True)
