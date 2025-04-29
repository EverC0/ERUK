import base64, io
<<<<<<< HEAD
from flask import Blueprint, render_template, url_for, redirect, request, flash, current_app
from flask_login import current_user, login_required
from mongoengine.queryset.visitor import Q

from .. import post_client
from ..forms import PostForm, CommentForm, SearchForm
from ..models import User, Post, Comment
from ..utils import current_time
=======
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

>>>>>>> a0997d9a870d24891f1182c64ee02a777f4e41e9

posts = Blueprint("posts", __name__) 

def get_b64_img(username):
    user = User.objects(username=username).first()
    if user and user.profile_pic:
        try:
            bytes_im = io.BytesIO(user.profile_pic.read())
            image = base64.b64encode(bytes_im.getvalue()).decode()
            return image
        except:
            return None
    return None

@posts.route("/", methods=["GET", "POST"])
def index():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("posts.query_results", query=form.search_query.data))
    
    # Get recent posts for the feed
    recent_posts = post_client.get_recent_posts(20)
    
    return render_template("index.html", form=form, posts=recent_posts)

<<<<<<< HEAD
@posts.route("/search-results/<query>", methods=["GET"])
def query_results(query):
    try:
        results = post_client.search(query)
        return render_template("query.html", results=results, query=query)
    except ValueError as e:
        return render_template("query.html", error_msg=str(e), query=query)
=======
@posts.route("/search/<category>")
def search_by_category(category):
    valid_categories = ["sports", "news", "entertainment"]
    if category.lower() not in valid_categories:
        flash("Invalid category.", "danger")
        return redirect(url_for("posts.index"))

    posts = Post.objects(category=category.lower())
    return render_template("search_results.html", posts=posts, category=category)

>>>>>>> a0997d9a870d24891f1182c64ee02a777f4e41e9

@posts.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
<<<<<<< HEAD
        # Create a new post
        new_post = Post(
            author=current_user._get_current_object(),
            content=form.content.data,
            category=form.category.data,
            date=current_time()
        )
        
        # Handle image upload if provided
        if form.image.data:
            new_post.image.put(form.image.data, content_type=form.image.data.content_type)
        
        new_post.save()
        flash("Post created successfully!", "success")
        return redirect(url_for("posts.index"))
=======
            
        new_post = Post(
        author=current_user._get_current_object(),
        content=form.content.data,
        category=form.category.data,
        )

        if form.image.data:
            new_post.image.put(form.image.data, content_type=form.image.data.content_type)

        new_post.save()

        return redirect(url_for("posts.post_detail", post_id=str(new_post.id)))
>>>>>>> a0997d9a870d24891f1182c64ee02a777f4e41e9
    
    return render_template("userPost.html", form=form)

<<<<<<< HEAD
@posts.route("/post/<post_id>", methods=["GET", "POST"])
def post_detail(post_id):
    try:
        post = post_client.retrieve_post_by_id(post_id)
    except ValueError as e:
        flash(str(e), "error")
        return redirect(url_for("posts.index"))
    
    # Handle commenting
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            post=post,
            commenter=current_user._get_current_object(),
            content=form.content.data,
            date=current_time()
        )
        comment.save()
        return redirect(url_for("posts.post_detail", post_id=post_id))
    
    # Fetch comments for this post
    comments = Comment.objects(post=post)
    
    # Get author's profile pic
    author_pic = get_b64_img(post.author.username)
    
    return render_template(
        "post_detail.html", 
        form=form, 
        post=post, 
        comments=comments, 
        author_pic=author_pic
    )

@posts.route("/category/<category>")
def category_posts(category):
    posts = post_client.get_posts_by_category(category)
    return render_template("category.html", posts=posts, category=category)
=======
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


>>>>>>> a0997d9a870d24891f1182c64ee02a777f4e41e9

@posts.route("/user/<username>")
def user_detail(username):
    user = User.objects(username=username).first()
    
    if not user:
        return render_template("user_detail.html", error="User not found.")
    
    posts = post_client.get_user_posts(user)
    image = get_b64_img(username)
    
    return render_template(
        "user_detail.html", 
        user=user, 
        posts=posts, 
        image=image, 
        error=None
    )
