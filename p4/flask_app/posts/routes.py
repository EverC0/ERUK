import base64, io
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from ..forms import PostForm, SearchForm, CommentForm  # Changed form
from ..models import User, Post  # Changed model
from ..utils import current_time
from ..aws import upload_file  # ✅
from flask_login import login_required
from .. import PostClient
from ..models import Post, PostComment
from flask import send_file
import io


posts = Blueprint("posts", __name__)

# Helper function remains similar
def get_b64_img(username):
    user = User.objects(username=username).first()
    if user and user.profile_pic:
        bytes_im = io.BytesIO(user.profile_pic.read())
        return base64.b64encode(bytes_im.getvalue()).decode()
    return None

# Updated view functions
@posts.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("posts.query_results", query=form.search_query.data))
    return render_template("index.html", form=form)

@posts.route("/search/<category>")
def search_by_category(category):
    valid_categories = ["sports", "news", "entertainment"]
    if category.lower() not in valid_categories:
        flash("Invalid category.", "danger")
        return redirect(url_for("posts.index"))

    posts = Post.objects(category=category.lower())
    return render_template("search_results.html", posts=posts, category=category)


@posts.route("/create-post", methods=["GET", "POST"])  # New post creation
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
            
        new_post = Post(
        author=current_user._get_current_object(),
        content=form.content.data,
        category=form.category.data,
        )

        if form.image.data:
            new_post.image.put(form.image.data, content_type=form.image.data.content_type)

        new_post.save()

        return redirect(url_for("posts.post_detail", post_id=str(new_post.id)))
    
    return render_template("userPost.html", form=form)

@posts.route("/post/<post_id>", methods=["GET", "POST"])  # ✅ ALLOW POST HERE
def post_detail(post_id):
    post = Post.objects.get_or_404(id=post_id)
    comments = PostComment.objects(post=post.id)
    form = CommentForm()

    if form.validate_on_submit() and current_user.is_authenticated:
        comment = PostComment(
            commenter=current_user._get_current_object(),
            post=post,
            content=form.content.data
        )
        comment.save()
        flash("Comment added!", "success")
        return redirect(url_for("posts.post_detail", post_id=post.id))

    return render_template("post_detail.html", post=post, comments=comments, comment_form=form)



@posts.route("/post/<post_id>/image")
def serve_image(post_id):
    post = Post.objects.get_or_404(id=post_id)

    if post.image:
        return send_file(
            io.BytesIO(post.image.read()),
            mimetype=post.image.content_type
        )
    else:
        return "No image found", 404



@posts.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first_or_404()
    user_posts = Post.objects(author=user)  # Changed from reviews
    return render_template("user_detail.html", 
                         user=user, 
                         posts=user_posts,
                         profile_image=get_b64_img(username))