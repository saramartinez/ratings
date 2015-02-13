from flask import Flask, render_template, redirect, request, session, flash, url_for
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

@app.route("/logout")
def logout():
    session['user'] = {}
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
def view_movie(id):
    movie_info = modelsession.query(Movie).get(id)
    ratings = movie_info.ratings
    rating_nums = []
    user_rating = None

    for r in ratings:
        if r.user_id == session['user']:
            user_rating = r
        rating_nums.append(r.rating)
    avg_rating = float(sum(rating_nums))/len(rating_nums)

    # Prediction code: only predict if the user hasn't rated it.
    user = modelsession.query(User).get(session['user'])
    prediction = None
    if not user_rating:
        prediction = user.predict_rating(movie_info)
    # End prediction

    return render_template("movie_info.html", movie=movie_info, 
            average=avg_rating, rating=user_rating,
            prediction=prediction)

@app.route("/rate/<int:id>", methods=["GET", "POST"])
def rate_movie(id):
    movie_info = modelsession.query(Movie).get(id)
    new_rating = request.form.get('new-rating', None)
    update_rating = request.form.get('update-rating', None)

    if 'user' in session:
        rating = modelsession.query(Rating).filter(Rating.user_id == session['user'], Rating.movie_id == id).first()

        if update_rating != None:
            rating.rating = update_rating
            flash("Your rating has been updated!")

        if new_rating != None:
            rating = Rating(user_id = session['user'], movie_id = movie_info.id, rating = new_rating)
            modelsession.add(rating)
            flash("Your rating has been added!")

        modelsession.commit()

        if rating or new_rating:
            modelsession.refresh(rating)

    else:
        rating = "You need to log in to utilize this feature!"

    return render_template("movie_info.html", movie = movie_info, rating=rating)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/search", methods=["POST"])
def search_results():
    query = request.form.get('query')
    results = modelsession.query(Movie).filter(Movie.title.like("%" + query + "%")).limit(50).all()

    return render_template("movie_list.html", movies=results)


if __name__ == "__main__":
    app.run(debug = True)