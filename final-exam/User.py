
secret = "kjasbdf3098r2yiwbfsaboibdsaf3298"

class User(db.Model):
    username=db.StringProperty(required=True)
    password=db.StringProperty(required=True)
    email=db.StringProperty()

    def make_salt():
	return ''.join(random.choice(string.letters) for x in xrange(10))

    def make_pw_hash(name, pw, salt=None):	
        if not salt:
            salt = make_salt()
    	    h = hashlib.sha256(name + pw + salt).hexdigest()
    	    return '%s,%s' % (h, salt)

    def valid_pw(name, pw, h):
        salt = h.split(',')[1]
    	return h == make_pw_hash(name, pw, salt)

    def valid_username(username):
	USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
    	return username and USER_RE.match(username)

    def valid_password(password):
	PASS_RE = re.compile(r"^.{3,20}$")
        return password and PASS_RE.match(password)

    def valid_email(email):
	EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
	return not email or EMAIL_RE.match(email)

    def create_hash(value):
	hash_value = hmac.new(secret, value).hexdigest()
	return '%s|%s' % (value, hash_value)

    def check_hash(value):
	val = value.split('|')[0]
        if value == create_hash(val):
            return True
        else:
            return False

    def addUser(username,password,email):
	
