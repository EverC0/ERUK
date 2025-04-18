import base64,io
from io import BytesIO
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user

from .. import movie_client
from ..forms import MovieReviewForm, SearchForm
from ..models import User, Review
from ..utils import current_time

""" ************ Blueprint must be chnaged to Social-POST ************ """
# 

movies = Blueprint("ok", __name__)
""" ************ Helper for pictures uses username to get their profile picture************ """
def get_b64_img(username):
    user = User.objects(username=username).first()
    bytes_im = io.BytesIO(user.profile_pic.read())
    image = base64.b64encode(bytes_im.getvalue()).decode()
    return image

""" ************ View functions ************ """


@movies.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()

    if form.validate_on_submit():
        return redirect(url_for("ok.query_results", query=form.search_query.data))

    return render_template("index.html", form=form)


@movies.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        # search for posts based on genre
        results = movie_client.search(query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e))

    return render_template("query.html", results=results)


@movies.route("/movies/<movie_id>", methods=["GET", "POST"])
# post details
def movie_detail(movie_id):
    try:
        result = movie_client.retrieve_movie_by_id(movie_id)
    except ValueError as e:
        return render_template("movie_detail.html", error_msg=str(e))

    form = MovieReviewForm()
    if form.validate_on_submit():
        review = Review(
            commenter=current_user._get_current_object(),
            content=form.text.data,
            date=current_time(),
            imdb_id=movie_id,
            movie_title=result.title,
        )

        review.save()

        return redirect(request.path)

    review_objects = Review.objects(imdb_id=movie_id)

    reviews = []
    for review in review_objects:
        commenter = review.commenter
        image = None

        if commenter.profile_pic.get() is not None:
            bytes_io = io.BytesIO(commenter.profile_pic.read())
            image = base64.b64encode(bytes_io.getvalue()).decode()

        review.image = image  # dynamically attach `image` attribute
        reviews.append(review)

    return render_template(
        "movie_detail.html", form=form, movie=result, reviews=reviews, error=None
    )


@movies.route("/user/<username>")
def user_detail(username):
    #uncomment to get review image
    user = User.objects(username=username).first()
    #find first match in db

    if not user:
        return render_template("user_detail.html", error="User not found.")

    reviews = Review.objects(commenter=user)
    image = None
    if user.profile_pic:
        try:
            bytes_io = io.BytesIO(user.profile_pic.read())
            image = base64.b64encode(bytes_io.getvalue()).decode()
        except:
            pass

    return render_template("user_detail.html", user=user, reviews=reviews, image=image, error=None)
    #use their username for helper function

