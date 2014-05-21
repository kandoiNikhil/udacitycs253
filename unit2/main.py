#!/usr/bin/env python
import webapp2
import cgi
import re
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASS_RE = re.compile(r"^.{3,20}$")
EMAIL_RE=re.compile("^[\S]+@[\S]+\.[\S]+$")
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
welcome_form="""
   <h2>Welcome, %(username)s !</h2>
"""

signup_form="""
   <h2>Signup</h2>
    <form method="post">
      <table>
        <tr>
          <td class="label">
            Username
          </td>
          <td>
            <input type="text" name="username" value="%(username)s">
          </td>
          <td class="error">
 	%(username_error)s           
          </td>
        </tr>

        <tr>
          <td class="label">
            Password
          </td>
          <td>
            <input type="password" name="password" value="">
          </td>
          <td class="error">
        %(password_error)s           
          </td>
        </tr>

        <tr>
          <td class="label">
            Verify Password
          </td>
          <td>
            <input type="password" name="verify" value="">
          </td>
          <td class="error">
            %(verify_error)s            
          </td>
        </tr>

        <tr>
          <td class="label">
            Email (optional)
          </td>
          <td>
            <input type="text" name="email" value="%(email)s">
          </td>
          <td class="error">
            %(email_error)s           
          </td>
        </tr>
      </table>

      <input type="submit">
    </form>
 

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
class SignUpHandler(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-type']='text/html'
		self.response.out.write(signup_form%{'username_error':'','password_error':'','verify_error':'','email_error':'','username':'','email':''})
	def post(self):
		v_u=False
		v_p=False
		v_v=False
		v_e=False
		self.response.headers['Content-Type']='text/html'
		username=self.request.get('username')
		password=self.request.get('password')
		verify=self.request.get('verify')
		email=self.request.get('email')
		username_error=""
		password_error=""
		verify_error=""
		email_error=""
		if valid_username(username):
			username_error=""
			v_u=True
		else:
			username_error="That's not a valid Username."


		if valid_password(password):
			password_error=""
			v_p=True
		else:
			password_error="That wasn't a valid Password."



		if verify !=password:
			verify_error="Your passwords didn't match."
		else:
			v_v=True


		if email:
			if not valid_email(email):
				email_error="That's not a valid email."
			else:
				v_e=True
		else:
			v_e=True

		
		if v_u and v_p and v_v and v_e:
			redirect_string='/unit2/welcome?username='+username
			self.redirect(redirect_string)
		else:
			self.response.out.write(signup_form%{"username_error":username_error,"password_error":password_error,"verify_error":verify_error,"email_error":email_error,'username':username,'email':email})
class Welcome(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type']='text/html'
		self.response.out.write(welcome_form%{'username':self.request.get("username")})

app = webapp2.WSGIApplication([('/unit2/rot13', ROT13Handler),('/unit2/signup',SignUpHandler),('/unit2/welcome',Welcome)], debug=True)
