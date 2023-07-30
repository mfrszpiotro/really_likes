from app.movies import bp
from flask import request, render_template, url_for, redirect, flash, session
from app.movies.forms import SearchForm
from unidecode import unidecode
from app.extensions import db
from app.movies.models import Movie, commit_diff_descr


@bp.route("/movies", methods=["GET", "POST"])
def movies():
    search_form = SearchForm()
    films = []

    # Form submitting logic:
    if request.form.get("search_submit"):
        return redirect(url_for("movies", search=request.form.get("search_text")))

    elif request.form.get("search_reset"):
        return redirect(url_for("movies"))

    else:
        films = db.session.execute(db.select(Movie).order_by(Movie.search)).scalars()
        commit_diff_descr(db, films, request.form.items())

    # View:
    search = unidecode(request.args.get("search", "")).strip().casefold()
    if search != "":
        films = db.session.execute(
            db.select(Movie)
            .order_by(Movie.search)
            .where(Movie.search.like("%" + search + "%"))
        ).scalars()
    else:
        films = db.session.execute(db.select(Movie).order_by(Movie.search)).scalars()
    return render_template("movies/movies.html", films=list(films), search_form=search_form)

# @bp.route("/movielist", methods=["GET", "POST"])
# def movielist():
#     # todo - not too elegant imo
#     if request.form.get("search_submit"):
#         books = db.session.execute(db.select(Book).order_by(Book.search).where(Book.check == "no")).scalars()
#         if len(list(books)) > 0:
#             flash("Natka nie ma jeszcze kilku książek...", "error")
#             books = db.session.execute(db.select(Book).order_by(Book.search).where(Book.check == "no")).scalars()
#             return render_template("booklist.html", books=list(books))
#         flash("Natka ma już wszystkie ksiązki!", "success")

#     # todo - not too elegant imo
#     elif request.form.get("search_reset"):
#         books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
#         return render_template("booklist.html", books=list(books))
    
#     elif request.form.__len__() > 0:
#         books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
#         commit_diff_check(db, books, request.form.items())
#     books = db.session.execute(db.select(Book).order_by(Book.search)).scalars()
#     return render_template("booklist.html", books=list(books))