from app.models import User
from app import app, db
import hashlib
import cloudinary.uploader


def auth_user(username, password, role=None):
	password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

	u = User.query.filter(User.username.__eq__(username.strip()),
						  User.password.__eq__(password))
	if role:
		u = u.filter(User.user_role.__eq__(role))

	return u.first()


def add_user(name, username, password, avatar):
	password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

	u = User(name=name, username=username, password=password,
			 avatar='https://res.cloudinary.com/dxxwcby8l/image/upload/v1690528735/cg6clgelp8zjwlehqsst.jpg')

	if avatar:
		res = cloudinary.uploader.upload(avatar)
		u.avatar = res.get('secure_url')

	db.session.add(u)
	db.session.commit()


def get_user_by_id(id):
	return User.query.get(id)
