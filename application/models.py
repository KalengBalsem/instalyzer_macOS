from . import db

class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, unique=True)
    username = db.Column(db.String(30), unique=True)
    full_name = db.Column(db.String(120))
    category = db.Column(db.String(120), nullable=False, default='Default Account')
    posts_count = db.Column(db.Integer, nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    following = db.Column(db.Integer, nullable=False)
    profile_picture = db.Column(db.String(999), nullable=False, default='default.jpg') #the default isn't configured yet
    no_of_highlights = db.Column(db.Integer, nullable=True)
    bio = db.Column(db.String(150), nullable=False, default='')
    bio_link = db.Column(db.String(150), nullable=False, default='')
    is_private = db.Column(db.Boolean, default=False, nullable=False)

    # one to many database (Profile <- Post)
    posts = db.relationship('Post', backref='owner')

class Post(db.Model):
    # main info
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, nullable=False)
    post_type = db.Column(db.String(30), nullable=False)
    display_url = db.Column(db.String(999), nullable=False)
    caption = db.Column(db.String(2200), nullable=False, default='')
    hashtags = db.Column(db.String(2200), nullable=False, default='')
    likes_count = db.Column(db.Integer, nullable=False)
    comments_count = db.Column(db.Integer, nullable=False)
    url = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.String(30), nullable=False)

    # one to many database (Post -> Profile)
    owner_id = db.Column(db.Integer, db.ForeignKey('profile.id'))

    # additional (not yet configured):

    # child_posts = db.Column(db.String(999), nullable=True)
    # tagged_users = db.Column(db.String(999), nullable=True)
    # music = db.Column(db.String(999), nullable=True)
    # video_play_count  = db.Column(db.Integer, nullable=True)
    # video_view_count  = db.Column(db.Integer, nullable=True)
    # video_duration = db.Column(db.Integer, nullable=True)
    # video_url = db.Column(db.String(999), nullable=True)

    
