from w3lib.html import replace_escape_chars
from datetime import datetime
import requests                             # to get profile picture

def get_profile_picture(url, username):
    img = requests.get(url).content
    with open(f'scraper/profile_pictures/{username}.jpg', 'wb') as file:
        file.write(img)
    return f'scraper\profile_pictures\{username}.jpg'


def parse_profile(json_file):
    user_data = json_file['data']['user']

    username = user_data['username']
    bio = user_data['biography']
    bio_link = user_data['bio_links']

    # useful functions
    def get_bio_link(bio_link):
        if not bio_link == []:
            url = bio_link[0]['url']
            return url 

    def get_profile_picture(url, username):
        img = requests.get(url).content
        with open(f'application/static/profile_pictures/{username}.jpg', 'wb') as file:
            file.write(img)
        return f'/static/profile_pictures/{username}.jpg'
    ####

    profile_data =  {
        "id": user_data['id'],
        "username": username,
        "full_name": user_data['full_name'],
        "category": user_data['category_name'],
        "posts_count":user_data['edge_owner_to_timeline_media']['count'],
        "followers":user_data['edge_followed_by']['count'],
        "following":user_data['edge_follow']['count'],
        "profile_picture": get_profile_picture(user_data['profile_pic_url_hd'], username),
        "no_of_highlights": user_data['highlight_reel_count'],
        "bio": replace_escape_chars(bio,replace_by=" "),
        "bio link": get_bio_link(bio_link),
        "is_private": user_data['is_private']
    }

    return profile_data

def parse_posts(json_file, username):
    user_data = json_file['data']['user']
    timeline = user_data['edge_owner_to_timeline_media']
    posts_edges = timeline['edges']
    posts_data = {}

    for i, post in enumerate(posts_edges):
        post = post['node']

        # required variables
        try:
            caption = post['edge_media_to_caption']['edges'][0]['node']['text']
        except:
            caption = ''
        shortcode = post['shortcode']

        # decode timestamp
        encrypted_timestamp = post['taken_at_timestamp']
        timestamp = datetime.fromtimestamp(encrypted_timestamp).strftime("%d/%m/%Y %H:%M:%S")
        
        node = f'{i}'
        posts_data[node] = {
            # main info

            'post_id': post['id'],
            'post_type': post['__typename'],
            'display_url': post['display_url'],
            'caption': caption,
            'hashtags': [i for i in caption.split() if i.startswith('#')],
            'likes_count': post['edge_media_preview_like']['count'],
            'comments_count': post['edge_media_to_comment']['count'],
            'url': f'https://www.instagram.com/{username}/p/{shortcode}/',
            'timestamp': timestamp

            # additional:

            # 'child_posts' = 
            # 'tagged_users' = 
            # 'music' = 
            # 'video_play_count' = 
            # 'video_view_count' = 
            # 'video_duration' = 
            # 'video_url' = 
        }
    return posts_data