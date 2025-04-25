from mongoengine.queryset.visitor import Q
from .models import Post

# class Post(db.Document):
#     author = ReferenceField(User, required=True)
#     content = StringField(required=True, min_length=5, max_length=500)
#     category = StringField(required=True, choices=["sports", "news", "entertainment"])  # New field
#     image = ImageField()  # Replace movie poster with user-uploaded image
#     date = StringField(default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
#     Unique ID = 

class PostClient:
    # mongodb connection and create a session
    """
    Client for interacting with Post objects in the database.
    Replaces the MovieClient that was used for OMDB API.
    """
    
    def search(self, search_string):
        """
        Searches posts by category or content containing the search string
        Returns a list of Post objects
        """
        # Convert search string to lowercase for case-insensitive matching
        search_string = search_string.lower()
        
        # Check if search exactly matches any category
        categories = ['sports', 'news', 'entertainment']
        if search_string in categories:
            # Exact category match - prioritize these results
            return Post.objects(category=search_string).order_by('-date')
        
        # Otherwise search by content and category
        return Post.objects(
            Q(content__icontains=search_string) | 
            Q(category__icontains=search_string)
        ).order_by('-date')
    
    def retrieve_post_by_id(self, post_id):
        """
        Retrieves a specific post by its ID
        Returns a Post object if found, raises ValueError if not found
        """
        try:
            post = Post.objects.get(id=post_id)
            return post
        except:
            raise ValueError(f"Post with ID {post_id} not found")
    
    def get_posts_by_category(self, category):
        """
        Returns all posts in a specific category
        """
        return Post.objects(category=category.lower()).order_by('-date')
    
    def get_recent_posts(self, limit=20):
        """
        Returns the most recent posts
        """
        return Post.objects().order_by('-date')[:limit]
    
    def get_user_posts(self, user):
        """
        Returns all posts by a specific user
        """
        return Post.objects(author=user).order_by('-date')
