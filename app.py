from flask import Flask, render_template, request, url_for, session, redirect
import bcrypt
from db.db import Connection

app = Flask(__name__)
app.secret_key = "terserah1234"


conn = Connection()


@app.route('/')
def home():
	navigation = {
		"Home" : "/"
	}
	active = "dashboard"
	return render_template("home/home.html", navigation=navigation, active=active)


@app.route('/login', methods=["GET", "POST"])
def login():
	navigation = {
		"Account" : "#",
		"Login" : "/login"
	}
	active = "account"
	if request.method == "POST":
		req = request.form

		email = req.get("email")
		password = req.get("password")

		result = conn.read('SELECT * FROM user WHERE user.email="%s"' % (email))

		if len(result) > 0:
			res = result[0]
			if password == res[4]:
				session['name'] = res[1]
				session['email'] = res[3]
				return redirect(url_for("home"))
			else:
				session.clear()
				return redirect(request.url)
		else:
			session.clear()
			return redirect(request.url)

	return render_template("auth/login.html", navigation=navigation, active=active)


@app.route('/register', methods=["GET", "POST"])
def register():
	navigation = {
		"Account" : "#",
		"Register" : "/register"
	}
	active = "account"

	if request.method == "POST":
		req = request.form
		
		first_name = req.get("first_name")
		last_name = req.get("last_name")
		email = req.get("email")
		password = req.get("password")

		msg = conn.change('INSERT INTO user (first_name, last_name, email, password, is_admin) VALUES ("%s", "%s", "%s", "%s", 0)' % (first_name, last_name, email, password))
		print(msg)
		if msg == "success":
			session['name'] = first_name
			return redirect(url_for("home"))
		else:
			return redirect(request.url)

	return render_template("auth/register.html", navigation=navigation, active=active)


@app.route('/logout')
def logout():
	session.clear()
	return redirect(url_for("home"))


if __name__ == '__main__':
	app.run(debug=True)