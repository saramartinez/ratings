from flask import Flask, render_template, redirect, request, session, flash
import model

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


# Create a new user (sign up)
@app.route("/sign-up", methods=['GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        pass
# def create_user(email, password):
#     # check if user in database & redirect to login
#     # else create new user / add to database
#     u = model.session.query(model.User).filter(model.User.email==email)
#     existing_user = u.one()
#     if existing_user:
#         flash("Your email address is already associated with an account. Please log in.")
#         redirect("login.html")
#     else:
#         #add to database
#         pass


# Allow existing users to log in
@app.route("/login", methods=['GET'])
def show_login():

    if "user" in session:
        flash("You're already logged in! Start rating movies!")
        return redirect('/')
    else:
        return render_template('login.html') 


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


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""

    email= request.form.get("email")
    password = request.form.get("password")
    customer = model.get_customer_by_email(email)

    if customer == None:
        flash("No user with this email exists!")
        return render_template("login.html")
    else:
        if password != customer.password:
            flash("Incorrect password. Please try again.")
            return render_template("login.html")
        else:
            session["user"]={"name":customer.name,"email":customer.email, "password":customer.password}
            g.display = session["user"]["name"]
            flash("Login successful!")
            return redirect("/melons")




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