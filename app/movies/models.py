from app.extensions import db


# api imdb movies
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    seen = db.Column(db.String, nullable=False)
    orig_title = name = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    search = db.Column(db.String, nullable=False)
    img = db.Column(db.String, nullable=True)
    appear_type = db.Column(db.String, nullable=False)
    job = db.Column(db.String, nullable=False)
    descr = db.Column(db.String, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    runtime = db.Column(db.String, nullable=True)


def commit_diff_descr(database, movies, form_movies):
    diffs = get_diff(extract_db_descr(movies), list(form_movies))
    for d in diffs:
        db_movie = database.session.execute(
            db.select(Movie).where(Movie.id == int(d[0]))
        ).scalar_one()
        db_movie.descr = d[1]
        database.session.commit()


def extract_db_descr(db_list):
    return [(str(db_item.id), db_item.descr) for db_item in db_list]


def get_diff(tuple_list_db, tuple_list_form):
    return [fd for fd in tuple_list_form if fd not in tuple_list_db]
