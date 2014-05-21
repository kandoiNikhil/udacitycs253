#!/usr/bin/env python
import webapp2
import cgi
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE=re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
	return USER_RE.match(username)
def valid_password(password):
	return PASS_RE.match(password)
def valid_email(email):
	return EMAIL_RE.match(email)
form="""
<p>Enter some text to ROT13:</p>
<form method="post">
<textarea name="text" style="height: 100px;width :400px;">%s</textarea>
<br>
<input type="submit">
</form >
"""

class ROT13Handler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type']='text/html'
		self.response.out.write(form%'')
	def post(self):
		self.response.headers['Content-Type']='text/html'
		inpt=self.request.get("text")
		inpt=self.rot13(inpt)
		inpt = cgi.escape(inpt,quote=True)
		self.response.headers['Content-Type']='text/html'
		self.response.out.write(form%inpt)
	def rot13(self,inpt):
		output=''
		for char in inpt:
			if char:

				if ord(char) >=97 and ord(char) <=122:
					value = (((ord(char)-97)+13)%26)+97
					output=output+chr(value)
				elif ord(char) >=65 and ord(char) <=90:
					value =  (((ord(char)-65)+13)%26)+65
					output=output+chr(value)
				else:
					output=output+char
			else:
				output=output+' '

		return output

class SignUpHandler:
	def get(self):
		self.response.headers['Content-type']='text/html'
		self.response.out.write('signup-form.html')
app = webapp2.WSGIApplication([('/unit2/rot13', ROT13Handler) , ('/unit2/signup',SignUpHandler) ], debug=True)
