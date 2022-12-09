# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 2}
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace("movies")
genre_ns = api.namespace("genres")
director_ns = api.namespace("directors")


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class DirectorSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    director_id = fields.Int()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)


@movie_ns.route("/")
class MoviesView(Resource):
    def get(self):
        movies = Movie.query.all()
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id:
            director = Movie.query.filter(Movie.director_id == director_id)
            if not director:
                return "", 404
            return movies_schema.dump(director)
        elif genre_id:
            genre = Movie.query.filter(Movie.genre_id == genre_id)
            if not genre:
                return "", 404
            return movies_schema.dump(genre)
        else:
            if not movies:
                return "", 404
            return movies_schema.dump(movies)


@movie_ns.route("/<int:uid>")
class MovieView(Resource):
    def get(self, uid):
        movie_by_id = Movie.query.get(uid)
        if not movie_by_id:
            return "", 404
        return movie_schema.dump(movie_by_id)



if __name__ == '__main__':
    app.run(debug=True)
