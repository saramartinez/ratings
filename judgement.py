from flask import Flask, render_template, redirect, request
import model

app = Flask(__name__)

@app.route("/")
def index():
    user_list = model.session.query(model.User).limit(5).all()
    return render_template("user_list.html", users=user_list)


# Create a new user (sign up)
@app.route("/signup")
def create_user():
    # check if user in database & redirect to login
    # else create new user / add to database
    pass


# Allow existing users to log in
@app.route("/login")
def log_in():
    # query for username, password with .one() result
    pass

# View a list of all users
@app.route("/all-users")
def list_all_users():
    # same as current index
    pass


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