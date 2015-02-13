from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
import correlation

ENGINE = create_engine("sqlite:///ratings.db", echo=True)
session = scoped_session(sessionmaker(bind=ENGINE,
                                      autocommit = False,
                                      autoflush = False))

Base = declarative_base()
Base.query = session.query_property()


### Class declarations go here
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True)
    email = Column(String(64), nullable=True)
    password = Column(String(64), nullable=True)
    age = Column(Integer, nullable=True)
    zipcode = Column(String(15), nullable=True)

    def similarity(self, other):
        u_ratings = {}
        paired_ratings = []
        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.rating, r.rating) )

        if paired_ratings:
            return correlation.pearson(paired_ratings)
        else:
            return 0.0

    def predict_rating(self, movie):
        ratings = self.ratings
        other_ratings = movie.ratings
        similarities = [ (self.similarity(r.user), r) \
            for r in other_ratings ]
        similarities.sort(reverse = True)
        similarities = [ sim for sim in similarities if sim[0] > 0 ]
        if not similarities:
            return None
        numerator = sum([ r.rating * similarity for similarity, r in similarities ])
        denominator = sum([ similarity[0] for similarity in similarities ])
        prediction = (numerator/denominator)
        return prediction

    def __repr__(self):
        return "<User: id=%d, email=%s, password=%s, age=%d, zipcode=%s>" % (self.id, self.email, self.password, self.age, self.zipcode)

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key= True)
    title = Column(String(64))
    release_date= Column(DateTime)
    imdb_url = Column(String(100))

    def __repr__(self):
        return "<Movie: id=%d, title=%s, release_date=%s, imdb_url=%s>" % (self.id, self.title, self.release_date, self.imdb_url)

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey('movies.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    rating = Column(Integer)

    user = relationship("User", backref=backref("ratings", order_by=id))
    movie = relationship("Movie", backref=backref("ratings"))

    def __repr__(self):
        return "<Rating: id=%d, movie_id=%d, user_id=%d, rating=%d>" % (self.id, self.movie_id, self.user_id, self.rating)
### End class declarations

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()