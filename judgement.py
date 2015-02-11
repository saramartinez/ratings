from flask import Flask, render_template, redirect, request, session, flash
import model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


# Create a new user (sign up)
@app.route("/sign-up")
def create_user(email, password):
    # check if user in database & redirect to login
    # else create new user / add to database
    u = model.session.query(model.User).filter(model.User.email==email)
    existing_user = u.one()
    if existing_user:
        flash("Your email address is already associated with an account. Please log in.")
        redirect("login.html")
    else:
        #add to database
        pass


# Allow existing users to log in
@app.route("/log-in")
def log_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

    user = model.validate_user(email, password)

    if 'user' not in session:
        session['user'] = user.id

    flash("Successfully logged in!")
    return redirect("/all-users")


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