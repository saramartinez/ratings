import model
from model import User, Movie, Rating 
import csv

def load_users(session):
    with open('seed_data/u.user', 'rb') as user_file:
        reader = csv.reader(user_file, delimiter='|')
        for row in reader:
            user = User(id=row[0], email=None, password=None, age=row[1], zipcode=row[4])
            session.add(user)
    session.commit()

def load_movies(session):
    # use u.item
    pass

def load_ratings(session):
    # use u.data
    pass


def main(session):
    # You'll call each of the load_* functions with the session as an argument
    load_users(session)
    

if __name__ == "__main__":
    s = model.connect()
    main(s)