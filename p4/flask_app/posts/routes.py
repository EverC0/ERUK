import base64, io
from flask import Blueprint, render_template, url_for, redirect, request, flash
from flask_login import current_user
from ..forms import PostForm, SearchForm  # Changed form
from ..models import User, Post  # Changed model
from ..utils import current_time
from ..aws import upload_file  # ✅
from flask_login import login_required



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

@posts.route("/search-results/<query>")
def query_results(query):
    # Search posts by category or content
    results = Post.objects(
        Q(category=query) | 
        Q(content__icontains=query)
    )
    return render_template("query.html", results=results)

@posts.route("/create-post", methods=["GET", "POST"])  # New post creation
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        # Handle image upload to S3
        image_url = None
        if form.image.data:
            image_url = upload_file(form.image.data)
            
        new_post = Post(
            author=current_user._get_current_object(),
            content=form.content.data,
            category=form.category.data,
            image_url=image_url,
            date=current_time()
        ).save()
        
        return redirect(url_for("posts.post_detail", post_id=str(new_post.id)))
    
    return render_template("create_post.html", form=form)

@posts.route("/post/<post_id>")  # Changed from movies
def post_detail(post_id):
    post = Post.objects.get_or_404(id=post_id)
    return render_template("post_detail.html", post=post)

@posts.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first_or_404()
    user_posts = Post.objects(author=user)  # Changed from reviews
    return render_template("user_detail.html", 
                         user=user, 
                         posts=user_posts,
                         profile_image=get_b64_img(username))