from flask import Flask, render_template, redirect, request, session, flash
from model import session as modelsession
from model import User, Movie, Rating

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

@app.route("/")
def index():
    return render_template("index.html")


# Create a new user (sign up)
@app.route("/signup", methods=['GET'])
def show_signup():
    return render_template("signup.html")

@app.route("/signup", methods=['POST'])
def process_signup():
    new_email = request.form.get("email")
    new_password = request.form.get("password")

    existing_user = modelsession.query(User).filter(User.email==new_email).first()
    
    if existing_user == None:
        new_user = User(email=new_email, password=new_password)
        modelsession.add(new_user)
        modelsession.commit()
        session['user'] = new_user.id
        flash("Successfully created account. You can now rate movies!")
        return redirect("/")
    else:
        flash("Your email address is already associated with an account. Please log in.")
        return redirect("/login")


# Show if user is already logged in
@app.route("/login", methods=['GET'])
def show_login():
    if "user" in session:
        flash("You're already logged in! Start rating movies!")
        return redirect('/')
    else:
        return render_template('login.html') 

# Allow existing users to log in
@app.route("/login", methods=['POST'])
def process_login():
    email = request.form.get('email')
    password = request.form.get('password')

    validate_email = model.validate_email(email)

    if validate_email == None:
        flash("No user with that email exists. Signup!")
        return render_template("signup.html")
    else:
        if password != validate_email.password:
            flash("Incorrect password. Please try again.")
            return render_template("login.html")
        else:
            session['user'] = validate_email.id
            flash("Successfully logged in. Start rating movies!")
            return redirect("/")


# View a list of all users
@app.route("/all-users")
def list_all_users():
    user_list = model.session.query(model.User).limit(50).all()
    return render_template("user_list.html", users=user_list)


# Look at user's ratings
@app.route("/user-ratings")
def list_user_ratings():
    # click on user
    # view list of movies they've rated and the ratings
    pass


# Add or update personal ratings when viewing record of movie
@app.route("/rate")
def update_rating():
    # check if browser session exists for user
    # if so, allow user to add a new rating or update an old rating
    # make sure rating is actually attached to user's id in database
    pass

if __name__ == "__main__":
    app.run(debug = True)