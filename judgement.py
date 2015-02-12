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
    if "user" not in session:
        return render_template("login.html")
    else:
        flash("You're already logged in! Start rating movies!")
        return redirect('/') 

# Allow existing users to log in
@app.route("/login", methods=['POST'])
def process_login():
    new_email = request.form.get('email')
    new_password = request.form.get('password')

    existing_user = modelsession.query(User).filter(User.email==new_email).first()

    if existing_user == None:
        flash("No user with that email exists. Signup!")
        return render_template("signup.html")
    else:
        if new_password != existing_user.password:
            flash("Incorrect password. Please try again.")
            return render_template("login.html")
        else:
            session['user'] = existing_user.id
            flash("Successfully logged in. Start rating movies!")
            return redirect("/")

# View a list of all users
@app.route("/users")
def list_all_users():
    user_list = modelsession.query(User).limit(50).all()
    return render_template("user_list.html", users=user_list)

# Look at user's ratings
@app.route("/users/<int:id>")
def list_user_ratings(id):
    ratings_list = modelsession.query(Rating).filter(Rating.user_id == id).all()
    return render_template("ratings_list.html", ratings = ratings_list, id = id)

@app.route("/movies")
def show_movies():
    movie_list = modelsession.query(Movie).limit(50).all()
    return render_template("movie_list.html", movies=movie_list)

@app.route("/movies/<int:id>", methods=["GET","POST"])
def movie(id):
    movie_info = modelsession.query(Movie).filter(Movie.id == id).first()

    new_rating = request.form.get('rating', None)

    if 'user' in session:
        rating = modelsession.query(Rating).filter(Rating.user_id == session['user'], Rating.movie_id == id).first()
        if new_rating != None:
            update_rating = Rating(user_id = session['user'], movie_id = movie_info.id, rating = new_rating)
            modelsession.add(update_rating)
            modelsession.commit()
            flash("Your rating has been updated!")
            return render_template("movie_info.html", movie = movie_info, rating=rating)

    else:
        rating = "You need to log in to utilize this feature!"

    return render_template("movie_info.html", movie = movie_info, rating=rating)


# Add or update personal ratings when viewing record of movie
@app.route("/rate")
def update_rating():
    # check if browser session exists for user
    # if so, allow user to add a new rating or update an old rating
    # make sure rating is actually attached to user's id in database
    pass

if __name__ == "__main__":
    app.run(debug = True)